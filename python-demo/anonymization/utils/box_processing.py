from . import convert_coordinate
from . import save_load
import tensorflow as tf
import numpy as np
import cv2 as cv

from object_detection.utils import visualization_utils as vis_util


def merge_boxes(img_height, img_width, boxes, threshold=0.1):
    boxes_copy = boxes.copy()
    locs = convert_coordinate.rel_to_abs(img_height, img_width, boxes_copy).tolist()

    flag = False
    while not flag:
        if_modify = False
        # reverse order is to avoid index out of bounds
        for i in range(len(locs)-1, 0, -1):
            x_min, y_min, x_max, y_max = locs[i]
            for j in range(i-1, 0, -1):
                x_min2, y_min2, x_max2, y_max2 = locs[j]

                # if IOU>0.3
                if __calculate_overlap(locs[i], locs[j]) > 0.3:
                    locs[i] = [min(x_min, x_min2), min(y_min, y_min2), max(x_max, x_max2), max(y_max, y_max2)]
                    del locs[j]
                    if_modify = True
                    break

                # if the two boxes are near to each other
                if __is_near(img_height, img_width, locs[i], locs[j]):
                    locs[i] = [min(x_min, x_min2), min(y_min, y_min2), max(x_max, x_max2), max(y_max, y_max2)]
                    del locs[j]
                    if_modify = True
                    break

            if if_modify:
                break
        if not if_modify:
            flag = True

    return locs


def clip_boxes(image_np, abs_boxes, file_name, output_dir, save=True):
    '''
    crop detected box from original image
    '''
    output_image = []
    abs_boxes = np.array(abs_boxes.copy())

    for i in range(abs_boxes.shape[0]):
        cropped_image = tf.image.crop_to_bounding_box(
                                                    image_np,
                                                    offset_height=int(abs_boxes[i, 0]),
                                                    offset_width=int(abs_boxes[i, 1]),
                                                    target_height=int(abs_boxes[i, 2] - abs_boxes[i, 0]),
                                                    target_width=int(abs_boxes[i, 3] - abs_boxes[i, 1])
                                                    )
        output_image.append(np.array(cropped_image))

    # save the clipped image
    if save:
        for i in range(len(output_image)):
            save_load.save_image(output_image[i], str(file_name) + '_box' + str(i), output_dir)

    return output_image


def calculate_position(ori_image_np, merged_box_position, boxes):
    '''
    calulate the location of detected human face and license plate in the original image
    '''
    x_min, y_min, x_max, y_max = merged_box_position
    img_h = x_max - x_min
    img_w = y_max - y_min
    abs_boxes = convert_coordinate.rel_to_abs(img_h, img_w, boxes)
    abs_boxes[:, 0:: 2] += x_min
    abs_boxes[:, 1:: 2] += y_min
    height, width = ori_image_np.shape[0], ori_image_np.shape[1]
    rel_boxes = convert_coordinate.abs_to_rel(height, width, abs_boxes)
    return rel_boxes


def show_inference(image_np, output_dict, label, threshold=0.5):
    vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      label,
      instance_masks=output_dict.get('detection_masks_reframed', None),
      use_normalized_coordinates=True,
      min_score_thresh=threshold,
      line_thickness=4)


def show_detected_boxes(image_np, boxes):
    image_copy = image_np.copy()
    boxes_copy = boxes.copy()
    im_height, im_length = image_np.shape[0], image_np.shape[1]
    abs_box = convert_coordinate.rel_to_abs(im_height, im_length, boxes_copy['detection_boxes'])
    for i in range(abs_box.shape[0]):
        y, x, bottom, right = abs_box[i]
        cv.rectangle(image_copy, (int(x), int(y)), (int(right), int(bottom)), (255, 255, 0), thickness=1)
        cv.putText(image_copy, "score:%.2f" % boxes_copy['detection_scores'][i], (int(x), int(y)-1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    return image_copy


def expand_boxes_area(img_height, img_width, abs_boxes, extend=10):
    '''
    expand the boundary of detection boxes
    '''
    for i in range(len(abs_boxes)):
        abs_boxes[i][0] = max(abs_boxes[i][0] - extend, 0)
        abs_boxes[i][1] = max(abs_boxes[i][1] - extend, 0)
        abs_boxes[i][2] = min(abs_boxes[i][2] + extend, img_height)
        abs_boxes[i][3] = min(abs_boxes[i][3] + extend, img_width)
    return abs_boxes


def __is_near(img_height, img_width, box1, box2, threshold=0.01):
    x_min, y_min, x_max, y_max = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if ((__is_small_box(img_height, img_width, box1)) or
       (__is_small_box(img_height, img_width, box2))):
        y_near = abs((y_min+y_max)/2-(y_min2+y_max2)/2) < threshold * img_height + (y_max-y_min)/2+(y_max2-y_min2)/2
        x_near = abs((x_min+x_max)/2-(x_min2+x_max2)/2) < threshold * img_width + (x_max-x_min)/2+(x_max2-x_min2)/2
        if y_near & x_near:
            return True
    return False


def __is_small_box(img_height, img_width, box, threshold=0.1):
    return ((box[3]-box[1]) < threshold*img_height) & ((box[2]-box[0]) < threshold*img_width)


def __calculate_overlap(box1, box2):
    x1, y1, x_max, y_max = box1
    x2, y2, x_max2, y_max2 = box2
    h1 = y_max - y1
    w1 = x_max - x1
    h2 = y_max2 - y2
    w2 = x_max2 - x2
    if(x1 > x2 + w2):
        return 0
    if(y1 > y2 + h2):
        return 0
    if(x1 + w1 < x2):
        return 0
    if(y1 + h1 < y2):
        return 0
    colInt = abs(min(x1 + w1, x2 + w2) - max(x1, x2))
    rowInt = abs(min(y1 + h1, y2 + h2) - max(y1, y2))
    overlap_area = colInt * rowInt
    area1 = w1 * h1
    area2 = w2 * h2
    return overlap_area / (area1 + area2 - overlap_area)