from anonymization import utils
from anonymization.image_processing import Img

import os.path
from object_detection.utils import ops as utils_ops
import tensorflow as tf
import time

"""
Example usage:
    python detect.py \
        --model_car_person_dir=res/model/car_person/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/saved_model/ \
        --model_face_license_dir=res/model/face_license/face_license2/saved_model/ \
        --threshold=0.2 \
        --detail=False\
        --input_dir=res/testimg/input/ \
        --output_dir=res/testimg/output/
"""

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# define name of flags
utils_ops.tf.app.flags.DEFINE_string('input_dir', 'res/testimg/input', 'Location of image folder for anonymization')
utils_ops.tf.app.flags.DEFINE_string('output_dir', 'res/testimg/output', 'Location of directory for results')
utils_ops.tf.app.flags.DEFINE_string('model_car_person_dir', 'res/model/car_person/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/saved_model', 'Location of saved_model folder for car and person')
utils_ops.tf.app.flags.DEFINE_string('model_face_license_dir', 'res/model/face_license/face_license2/saved_model', 'Location of saved_model folder for face and license')
utils_ops.tf.app.flags.DEFINE_float('threshold', '0.2', 'Value of detection threshold,default is 0.25', lower_bound=0.0, upper_bound=1.0)
utils_ops.tf.app.flags.DEFINE_bool('detail', 'False', 'Save output for each process during the detection')
FLAGS = utils_ops.tf.app.flags.FLAGS

# patch the location of gfile
tf.gfile = tf.io.gfile


def anonymization_process(model_car_person_dir,
                                                            model_face_license_dir,
                                                            threshold,
                                                            detail,
                                                            input_dir,
                                                            output_dir):

    TEST_IMAGE_PATHS = utils.save_load.get_image_paths(input_dir)
    model_car_person = utils.save_load.load_model(model_car_person_dir)
    model_face_license = utils.save_load.load_model(model_face_license_dir)

    counter = 0
    start = time.time()

    for img_path in TEST_IMAGE_PATHS:
        input_img = Img(img_path)
        name = os.path.splitext(os.path.basename(img_path))[0]
        input_img.detection_car_person(model_car_person)
        input_img.detection_face_license(model_face_license, threshold)
        blurred_img = input_img.blurring()

        if detail:
            # save detected car and person
            save_image = utils.box_processing.show_detected_boxes(input_img.image_np, input_img.boxes_list[0])
            utils.save_load.save_image(save_image, name, output_dir + 'car_person/')
            # save merged boxes as .jpg
            utils.box_processing.clip_boxes(input_img.image_np, input_img.merged_boxes, name, output_dir + 'merged_box/')
            # save detection results as .jpg
            if input_img.boxes_list[1]['detection_boxes'].shape[0] > 0:
                face_save_image = utils.box_processing.show_detected_boxes(input_img.image_np, input_img.boxes_list[1])
                utils.save_load.save_image(face_save_image, name, output_dir + 'face_license/')
            else:
                utils.save_load.save_image(input_img.image_np, name, output_dir + 'face_license/')
            # save box data as .txt for evaluation
            utils.save_load.save_detection_result(input_img, name, output_dir + 'box_position/')

        # save anonymiazed results
        utils.save_load.save_image(blurred_img, name, output_dir + 'anonymized/')
        counter += 1

    end = time.time()
    print(counter, 'images was anonymized')
    print('total time cost:% .2f s' % (end-start))
    print('average time cost: % .2f s' % ((end-start)/counter))


def main(_):
    anonymization_process(
      model_car_person_dir=FLAGS.model_car_person_dir,
      model_face_license_dir=FLAGS.model_face_license_dir,
      threshold=FLAGS.threshold,
      detail=FLAGS.detail,
      input_dir=FLAGS.input_dir,
      output_dir=FLAGS.output_dir)


if __name__ == '__main__':
    utils_ops.tf.app.run()
