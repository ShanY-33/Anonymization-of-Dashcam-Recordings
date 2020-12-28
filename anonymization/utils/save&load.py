import pathlib
import tensorflow as tf

from PIL import Image
from object_detection.utils import label_map_util


def get_image_paths(input_dir='../res/testimg/input'):
    PATH_TO_TEST_IMAGES_DIR = pathlib.Path(input_dir)
    TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))
    return TEST_IMAGE_PATHS


def save_image( image_np, file_name, output_dir='../res/testimg/output'):
    Image.fromarray(image_np).save(output_dir + str(file_name) + ".jpg")


def load_model(model_dir='../res/model/saved_model'):
    return(tf.saved_model.load(model_dir))


def load_label(label_path='../res/model/config/label_map.pbtxt'):
    return(label_map_util.create_category_index_from_labelmap(label_path, use_display_name=True))