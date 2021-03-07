import numpy as np


def rel_to_abs(img_h: int, img_w: int,  rel_box):
    """
    float location (range (0, 1)) to int location
    """
    abs_box = np.asarray(rel_box.copy())
    abs_box[:, 0:: 2] = img_h * abs_box[:, 0:: 2]
    abs_box[:, 1:: 2] = img_w * abs_box[:, 1:: 2]
    # Math.round
    abs_box += 0.5
    abs_box = abs_box.astype(int)
    return abs_box


def abs_to_rel(img_h: int, img_w: int, abs_box):
    """
    int location to float location (range (0, 1))
    """
    rel_box = abs_box.copy().astype(float)
    rel_box[:, 0:: 2] = rel_box[:, 0:: 2] / float(img_h)
    rel_box[:, 1:: 2] = rel_box[:, 1:: 2] / float(img_w)
    return rel_box


def xyxy_to_xyhw(abs_box):
    """
    (xmin, ymin, xmax, ymax) to (xmin, ymin, height, width)
    """
    abs_box = np.asarray(abs_box)
    abs_box[:, 2] = abs_box[:, 2] - abs_box[:, 0]
    abs_box[:, 3] = abs_box[:, 3] - abs_box[:, 1]
    abs_box.tolist()
    return abs_box


def xyhw_to_xyxy(abs_box):
    """
    (xmin, ymin, height, width) to (xmin, ymin, xmax, ymax)
    """
    abs_box = np.asarray(abs_box)
    abs_box[:, 2] = abs_box[:, 2] + abs_box[:, 0]
    abs_box[:, 3] = abs_box[:, 3] + abs_box[:, 1]
    abs_box.tolist()
    return abs_box
