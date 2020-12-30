# import anonymization
from anonymization import utils
from anonymization.image_processing import Img

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import tensorflow as tf

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

img_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/testimg/input'
model_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/ssd_v2_fpnlite/saved_model'
label_path = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/ssd_v2_fpnlite/config/mscoco_label_map.pbtxt'
output_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/testimg/output/'


TEST_IMAGE_PATHS = utils.save_load.get_image_paths(img_dir)

model = utils.save_load.load_model(model_dir)
label = utils.save_load.load_label(label_path)

counter = 0
for img_path in TEST_IMAGE_PATHS:
    input_img = Img(img_path)
    input_img.detection_car_person(model)
    # print(input_img.boxes_list[0]['detection_boxes'])  # car and person
    # print(input_img.merged_boxes)
    # utils.box_processing.clip_boxes(input_img.image_np, input_img.merged_boxes, 'img' + str(counter), output_dir)
    counter += 1
