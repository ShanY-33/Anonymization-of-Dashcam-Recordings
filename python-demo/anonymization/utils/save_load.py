import pathlib
import tensorflow as tf
from . import convert_coordinate
import numpy as np

from PIL import Image
from object_detection.utils import label_map_util


def get_image_paths(input_dir):
    PATH_TO_TEST_IMAGES_DIR = pathlib.Path(input_dir)
    TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))
    return TEST_IMAGE_PATHS


def save_image(image, file_name, output_dir):
    if type(image) == np.ndarray:
        Image.fromarray(image).save(output_dir + str(file_name) + ".jpg")
    else:
        image.save(output_dir + str(file_name) + ".jpg")


def load_model(model_dir):
    return(tf.saved_model.load(model_dir))


def load_label(label_path):
    return(label_map_util.create_category_index_from_labelmap(label_path, use_display_name=True))


def save_detection_result(image, file_name, output_dir):
    f = open(output_dir + file_name + ".txt", "w+")
    str_list = []
    if image.boxes_list[1]['detection_boxes'].shape[0] > 0:
        abs_box = convert_coordinate.rel_to_abs(image.height, image.width, image.boxes_list[1]['detection_boxes'])
    for i in range(image.boxes_list[1]['detection_boxes'].shape[0]):
        str_line = ""
        if image.boxes_list[1]['detection_classes'][i] == 1:
            str_line += "human_face" + " "
        elif image.boxes_list[1]['detection_classes'][i] == 2:
            str_line += "license_plate" + " "
        str_line += str(round(image.boxes_list[1]['detection_scores'][i], 5)) + " "
        str_line += str(abs_box[i, 1]) + " " + str(abs_box[i, 0]) + " " + str(abs_box[i, 3]) + " " + str(abs_box[i, 2])
        str_list.append(str_line)
    str_list = [line+'\n' for line in str_list]
    f.writelines(str_list)
    f.close()
