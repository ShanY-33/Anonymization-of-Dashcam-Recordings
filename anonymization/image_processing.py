from anonymization.utils import save_load
from anonymization.utils import merge_boxes
#from anonymization import utils
import numpy as np
from PIL import Image
import tensorflow as tf

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1
# Patch the location of gfile
tf.gfile = tf.io.gfile

THRESHOLD_CAR_PERSON = 0.5
THRESHOLD_FACE = 0.5
THRESHOLD_PLATE = 0.5
THRESHOLD_MERGE = 0.1


class Img():
    def __init__(self, image_path):
        self.image_np = np.asarray(Image.open(image_path))
        self.height = self.image_np.shape[0]
        self.width = self.image_np.shape[1]
        self.boxes_list = []  # boxes_list[0] --> car & person box, boxes_list[>0] --> subimage boxes
        self.merged_boxes = []
        self.subimg = []

    def detection_all_classes(self, model, threshold):
        image = np.asarray(self.image_np)
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

    def detection_car_person(self, model, threshold=THRESHOLD_CAR_PERSON, detection_classes=(1, 3, 4)):
        # 1: person; 3: car; 4: motorcycle; 6: bus; 8: truck
        output_dict = self.detection_all_classes(model, threshold)
        len = output_dict['detection_boxes'].shape[0]
        output_dict_list = output_dict.copy()
        output_dict_list['detection_boxes'] = (output_dict_list['detection_boxes']).tolist()
        output_dict_list['detection_classes'] =(output_dict_list['detection_classes']).tolist()
        output_dict_list['detection_scores'] = (output_dict_list['detection_scores']).tolist()

        for i in range(len-1, -1, -1):
            if (output_dict['detection_classes'][i] not in detection_classes or output_dict['detection_scores'][i] < threshold):
                del (output_dict_list['detection_boxes'])[i]
                del (output_dict_list['detection_classes'])[i]
                del (output_dict_list['detection_scores'])[i]

        self.boxes_list.append(output_dict)

        self.merged_boxes = merge_boxes.merge_boxes(self.height, self.width, self.boxes_list[0]['detection_boxes'])







    