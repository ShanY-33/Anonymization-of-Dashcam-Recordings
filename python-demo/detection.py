from anonymization import utils
from anonymization.image_processing import Img
import os.path

from object_detection.utils import ops as utils_ops

import tensorflow as tf

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

img_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/testimg/input'
output_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/testimg/output/'
TEST_IMAGE_PATHS = utils.save_load.get_image_paths(img_dir)

model_car_person_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/saved_model'
label_car_person_path = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/mscoco_label_map.pbtxt'
model_car_person = utils.save_load.load_model(model_car_person_dir)
# label_car_person = utils.save_load.load_label(label_car_person_path)

model_face_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/face/saved_model'
# label_face_license_path = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/face_license/config/label_map.pbtxt'
model_face = utils.save_load.load_model(model_face_dir)

model_face_license_dir = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/face_license2/saved_model'
# label_face_license_path = '/home/shanshan/github/Anonymization-of-Dashcam-Recordings/res/model/face_license/config/label_map.pbtxt'
model_face_license = utils.save_load.load_model(model_face_license_dir)
# label_face = utils.save_load.load_label(label_face_path)

counter = 0
for img_path in TEST_IMAGE_PATHS:
    input_img = Img(img_path)
    input_img.detection_car_person(model_car_person)

    # 存 car和person的框
    save_image = utils.box_processing.show_detected_boxes(input_img.image_np, input_img.boxes_list[0])
    utils.save_load.save_image(save_image, 'img' + str(counter), output_dir + 'car_person/')

    utils.box_processing.clip_boxes(input_img.image_np, input_img.merged_boxes, 'img' + str(counter), output_dir + 'box/')
    input_img.detection_face_license(model_face_license, threshold=0.2)

    # for j in range(1, len(input_img.boxes_list)):
    #     clip_area = utils.convert_coordinate.rel_to_abs(input_img.height, input_img.width, input_img.boxes_list[j]['detection_boxes'])
    #     utils.box_processing.clip_boxes(input_img.image_np, clip_area, 'img' + str(counter) + str(j), output_dir)
    #     face_save_image = utils.box_processing.show_detected_boxes(input_img.image_np, input_img.boxes_list[j])
    #     utils.save_load.save_image(face_save_image, 'img' + str(counter) + str(j), output_dir)
    if input_img.boxes_list[1]['detection_boxes'].shape[0] > 0:
        # clip_area = utils.convert_coordinate.rel_to_abs(input_img.height, input_img.width, input_img.boxes_list[1]['detection_boxes'])
        # utils.box_processing.clip_boxes(input_img.image_np, clip_area, 'box' + str(counter), output_dir)

        face_save_image = utils.box_processing.show_detected_boxes(input_img.image_np, input_img.boxes_list[1])
        utils.save_load.save_image(face_save_image, 'img_face_license' + str(counter), output_dir + 'face_license/')
    else:
        print('nothing was detected')

    name = os.path.splitext(os.path.basename(img_path))[0]
    utils.save_load.save_detection_result(input_img, name, output_dir + 'detection/')
    counter += 1