from anonymization.utils import box_processing
from anonymization.utils import convert_coordinate
import numpy as np
from PIL import Image, ImageFilter
import tensorflow as tf

from object_detection.utils import ops as utils_ops


# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1
# Patch the location of gfile
tf.gfile = tf.io.gfile

THRESHOLD_CAR_PERSON = 0.3
THRESHOLD_FACE_LICENSE = 0.2
THRESHOLD_MERGE = 0.1


class Img():
    def __init__(self, image_path):
        self.image_np = np.asarray(Image.open(image_path))
        self.height = self.image_np.shape[0]
        self.width = self.image_np.shape[1]
        self.boxes_list = []  # boxes_list[0] --> car & person box, boxes_list[1] --> face & license box
        self.merged_boxes = []
        self.subimg = []

    def gerneral_detection(self, img_np,  model, threshold):
        image = np.asarray(img_np)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run inference
        model_fn = model.signatures['serving_default']
        output_dict = model_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key: value[0, :num_detections].numpy() for key, value in output_dict.items()}
        output_dict['num_detections'] = num_detections

        # detection_classes should be ints.
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

        # Handle models with masks:
        if 'detection_masks' in output_dict:
            # Reframe the the bbox mask to the image size.
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    output_dict['detection_masks'], output_dict['detection_boxes'],
                    image.shape[0], image.shape[1])
            detection_masks_reframed = tf.cast(detection_masks_reframed > threshold, tf.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

        return(output_dict)

    def detection_car_person(self, model, threshold=THRESHOLD_CAR_PERSON, detection_classes=(1, 3, 4, 6, 8)):
        # run detection
        output_dict = self.gerneral_detection(self.image_np, model, threshold)

        len = output_dict['detection_boxes'].shape[0]
        output_dict_list = {}
        output_dict_list['detection_boxes'] = (output_dict['detection_boxes']).tolist()
        output_dict_list['detection_classes'] = (output_dict['detection_classes']).tolist()
        output_dict_list['detection_scores'] = (output_dict['detection_scores']).tolist()

        # remove the detection we don't need
        for i in range(len-1, -1, -1):
            # detection_class: 1: person; 3: car; 4: motorcycle; 6: bus; 8: truck
            if ((output_dict_list['detection_classes'][i] not in detection_classes) or (output_dict_list['detection_scores'][i] < threshold)):
                del (output_dict_list['detection_boxes'])[i]
                del (output_dict_list['detection_classes'])[i]
                del (output_dict_list['detection_scores'])[i]

        output_dict_list['detection_boxes'] = np.array(output_dict_list['detection_boxes'])
        output_dict_list['detection_classes'] = np.array(output_dict_list['detection_classes'])
        output_dict_list['detection_scores'] = np.array(output_dict_list['detection_scores'])

        self.boxes_list.append(output_dict_list)

        # merge and expand
        self.merged_boxes = box_processing.merge_boxes(self.height, self.width, self.boxes_list[0]['detection_boxes'])
        self.merged_boxes = box_processing.expand_boxes_area(self.height, self.width, self.merged_boxes)

    def detection_face_license(self, model, threshold=THRESHOLD_FACE_LICENSE):
        merged_boxes_copy = self.merged_boxes.copy()
        xyhw_box = convert_coordinate.xyxy_to_xyhw(merged_boxes_copy)
        temp_output_dict = {}
        temp_output_dict['detection_boxes'] = []
        temp_output_dict['detection_classes'] = []
        temp_output_dict['detection_scores'] = []

        # crop bounding boxes
        for i in range(len(xyhw_box)):
            x, y, h, w = xyhw_box[i]
            cropped_image = tf.image.crop_to_bounding_box(
                                                    self.image_np,
                                                    offset_height=x,
                                                    offset_width=y,
                                                    target_height=h,
                                                    target_width=w
                                                    )

            output_dict = self.gerneral_detection(cropped_image, model, threshold)

            len_dict = output_dict['detection_boxes'].shape[0]
            output_dict_list = {}
            output_dict_list['detection_boxes'] = (output_dict['detection_boxes']).tolist()
            output_dict_list['detection_classes'] = (output_dict['detection_classes']).tolist()
            output_dict_list['detection_scores'] = (output_dict['detection_scores']).tolist()

            # remove the bounding box with low confidence
            for j in range(len_dict-1, -1, -1):
                if (output_dict_list['detection_scores'][j] < threshold):
                    del (output_dict_list['detection_boxes'])[j]
                    del (output_dict_list['detection_classes'])[j]
                    del (output_dict_list['detection_scores'])[j]

            if len(output_dict_list['detection_boxes']) > 0:
                # map the bounding box back to the original image
                output_dict_list['detection_boxes'] = box_processing.calculate_position(self.image_np, self.merged_boxes[i], output_dict_list['detection_boxes'])
                for k in range(len(output_dict_list['detection_boxes'])):
                    temp_output_dict['detection_boxes'].append(output_dict_list['detection_boxes'][k])
                    temp_output_dict['detection_classes'].append(output_dict_list['detection_classes'][k])
                    temp_output_dict['detection_scores'].append(output_dict_list['detection_scores'][k])

        temp_output_dict['detection_boxes'] = np.array(temp_output_dict['detection_boxes'])
        temp_output_dict['detection_classes'] = np.array(temp_output_dict['detection_classes'])
        temp_output_dict['detection_scores'] = np.array(temp_output_dict['detection_scores'])
        self.boxes_list.append(temp_output_dict)

    def blurring(self):
        blurred_img = Image.fromarray(self.image_np)
        if self.boxes_list[1]['detection_boxes'].shape[0] > 0:
            abs_box = convert_coordinate.rel_to_abs(self.height, self.width, self.boxes_list[1]['detection_boxes'])
            for box in abs_box:
                clip_box = (box[1], box[0], box[3], box[2])
                clips = blurred_img.crop(clip_box).filter(ImageFilter.GaussianBlur(radius=5))
                blurred_img.paste(clips, clip_box)
        return blurred_img
