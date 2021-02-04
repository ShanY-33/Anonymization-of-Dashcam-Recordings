# Demo Code

## Overview
* `detection.py` aaaa
* `anonymization/` aaa
* `res/` aaa

## Requirements
### Python Packages
To use our software, you'll need to install several python packages. Please use `requirements.txt` to install the python packages:
```
pip install -r requirements.txt
```
### TensorFlow Object Detection API
Our detection framework is based on [TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection). We use the Object Detection API with TensorFlow 2.
Please find a detailed installation document [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2.md).



## Usage Example
```
python detection.py \
    --model_car_person_dir=res/model/car_person/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/saved_model \
    --model_face_license_dir=res/model/face_license/face_license2/saved_model \
    --threshold=0.2 \
    --input_dir=res/testimg/input/ \
    --output_dir=res/testimg/output/
```



