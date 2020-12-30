from . import convert_coordinate
from . import save_load
import tensorflow as tf
import numpy as np


def merge_boxes(img_height, img_width, boxes, threshold=0.1):
    '''
    merge bound boxes
    Args:
        locs-->list: [[x_min1,y_min1,x_max2,y_max2],...,[x_min1,y_min1,x_max2,y_max2]]
        w: the width of the image
        h: the height of the image
        thre: threshold for judging if two bound box is near enough
    '''

    locs = convert_coordinate.rel_to_abs(img_height, img_width, boxes).tolist()

    flag = False
    while not flag:
        if_modify = False
        for i in range(len(locs)-1):
            x_min, y_min, x_max, y_max = locs[i]
            for j in range(i+1, len(locs)):
                x_min2, y_min2, x_max2, y_max2 = locs[j]

                if __calculate_overlap( locs[i], locs[j]) > 0.3:
                    locs[i] = [min(x_min, x_min2), min(y_min, y_min2),max(x_max, x_max2),max(y_max, y_max2)]
                    del locs[j]
                    if_modify = True
                    break

                # near
                if __is_near(img_height, img_width, locs[i], locs[j]):
                        locs[i] = [min(x_min, x_min2),min(y_min, y_min2), max(x_max, x_max2),max(y_max, y_max2)]
                        del locs[j]
                        if_modify = True
                        break

                # include
                if __is_included(img_height, img_width, locs[i], locs[j]):
                    locs[i] = [min(x_min, x_min2), min(y_min, y_min2), max(x_max, x_max2), max(y_max, y_max2)]
                    del locs[j]
                    if_modify = True
                    break

            if if_modify:
                break
        if not if_modify:
            flag = True

    return locs


def clip_boxes(image_np, abs_boxes, file_name, output_dir, save=True, extend=10):
    im_height, im_length = image_np.shape[0], image_np.shape[1]
    output_image = []
    abs_boxes = np.array(abs_boxes)

    for i in range(abs_boxes.shape[0]):
        cropped_image = tf.image.crop_to_bounding_box(
                                                    image_np,
                                                    offset_height=int(max(abs_boxes[i, 0] - extend, 0)),
                                                    offset_width=int(max(abs_boxes[i, 1] - extend, 0)),
                                                    target_height=int(min(abs_boxes[i, 2] - abs_boxes[i, 0] + 2 * extend, im_height - abs_boxes[i, 0])),
                                                    target_width=int(min(abs_boxes[i, 3] - abs_boxes[i, 1] + 2 * extend, im_length - abs_boxes[i, 1]))
                                                    )
        output_image.append(np.array(cropped_image))

    if save:
        for i in range(len(output_image)):
            save_load.save_image(output_image[i], str(file_name) + '_box' + str(i), output_dir)
    
    return output_image


def calculate_position(merged_box_position, boxes):
    x_min, y_min, x_max, y_max = merged_box_position
    img_h = x_max - x_min
    img_w = y_max - y_min
    abs_boxes = convert_coordinate.rel_to_abs(img_h, img_w, boxes)
    abs_boxes[:, 0:: 2] += x_min
    abs_boxes[:, 1:: 2] += y_min
    rel_boxes = convert_coordinate.abs_to_rel(img_h, img_w, abs_boxes)
    return rel_boxes


def __is_almost_same_box(img_height, img_width, box1, box2, threshold=0.01):
    x_min, y_min, x_max, y_max = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if ((abs(x_min-x_min2) < threshold * img_width) and
       (abs(x_max-x_max2) < threshold * img_width) and
       (abs(y_max-y_max2) < threshold*img_height) and
       (abs(y_min-y_min2) < threshold*img_height)):
        return True
    return False


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


def __is_included(img_height, img_width, box1, box2, extend=0.01):
    x_min, y_min, x_max, y_max = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if ((__is_small_box(img_height, img_width, box1)) or
       (__is_small_box(img_height, img_width, box2))):
        if((x_min < x_min2 + extend * img_width and y_min < y_min2+extend*img_height and x_max > x_max2 - extend * img_width and y_max > y_max2-extend*img_height) or
           (x_min > x_min2 - extend * img_width and y_min > y_min2-extend*img_height and x_max < x_max2 + extend * img_width and y_max < y_max2 + extend * img_height)):
            return True
    return False


def __calculate_overlap(box1, box2):
    '''
    说明：图像中，从左往右是 x 轴（0~无穷大），从上往下是 y 轴（0~无穷大），从左往右是宽度 w ，从上往下是高度 h
    :param x1: 第一个框的左上角 x 坐标
    :param y1: 第一个框的左上角 y 坐标
    :param w1: 第一幅图中的检测框的宽度
    :param h1: 第一幅图中的检测框的高度
    :param x2: 第二个框的左上角 x 坐标
    :param y2:
    :param w2:
    :param h2:
    :return: 两个如果有交集则返回重叠度 IOU, 如果没有交集则返回 0
    '''
    x1, y1, x_max, y_max = box1
    x2, y2, x_max2, y_max2 = box2
    w1 = y_max - y1
    h1 = x_max - x1
    w2 = y_max2 - y2
    h2 = x_max2 - x2
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