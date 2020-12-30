import numpy as np


def rel_to_abs(img_h: int, img_w: int,  rel_box):
    abs_box = np.asarray(rel_box)
    abs_box[:, 0:: 2] = img_h * abs_box[:, 0:: 2]
    abs_box[:, 1:: 2] = img_w * abs_box[:, 1:: 2]
    abs_box = abs_box.astype(int)
    return abs_box


def abs_to_rel(img_h: int, img_w: int, abs_box):
    rel_box = abs_box.copy()
    rel_box[:, 0:: 2] = rel_box[:, 0:: 2] / float(img_h)
    rel_box[:, 1:: 2] = rel_box[:, 1:: 2] / float(img_w)
    return rel_box


def xyxy_to_xyhw(abs_box):
    # (xmin, ymin, height, width)
    abs_box[:, 2] = abs_box[:, 2] - abs_box[:, 0]
    abs_box[:, 3] = abs_box[:, 3] - abs_box[:, 1]
    return abs_box


def xyhw_to_xyxy(abs_box):
    # (xmin, ymin, xmax, ymax)
    abs_box[:, 2] = abs_box[:, 2] + abs_box[:, 0]
    abs_box[:, 3] = abs_box[:, 3] + abs_box[:, 1]
    return abs_box

