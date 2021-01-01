from . import convert_coordinate
import cv2 as cv


def show_detected_boxes(image_np, boxes):
    abs_box = convert_coordinate.rel_to_abs(boxes['detection_boxes'])
    for i in range(abs_box.shape[0]):
        x, y, right, bottom = abs_box[i]
        cv.rectangle(image_np, (int(x), int(y)), (int(right), int(bottom)), (255, 255, 0), thickness=2)
        cv.putText(image_np, "score:%.2f" % boxes['detection_scores'][i], (int(x), int(y)-1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    return image_np
