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
output_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/testimg/output/'
TEST_IMAGE_PATHS = utils.save_load.get_image_paths(img_dir)

model_car_person_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/ssd_v2_fpnlite/saved_model'
label_car_person_path = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/ssd_v2_fpnlite/config/mscoco_label_map.pbtxt'
model_car_person = utils.save_load.load_model(model_car_person_dir)
label_car_person = utils.save_load.load_label(label_car_person_path)

model_face_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/face/saved_model'
label_face_path = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/face/config/label_map.pbtxt'
model_face = utils.save_load.load_model(model_face_dir)
# label_face = utils.save_load.load_label(label_face_path)

counter = 0
for img_path in TEST_IMAGE_PATHS:
    input_img = Img(img_path)
    input_img.detection_car_person(model_car_person)
    utils.visual.show_inference(input_img.image_np, input_img.boxes_list[0],label_car_person)

    # utils.box_processing.clip_boxes(input_img.image_np, input_img.merged_boxes, 'img' + str(counter), output_dir)
    # input_img.detection_face_license(model_face)
    # for j in range(1, len(input_img.boxes_list)):
    #     utils.box_processing.clip_boxes(input_img.image_np, input_img.boxes_list[j]['detection_boxes'], 'img' + str(counter), output_dir, extend=0)
    # counter += 1
