# Python Demo Code

## Overview
* `detect.py` runs mdoel against given image and generates anonymized image
* `anonymization/` This directory contrains the main part of the code.
* `res/` This directory contains detection models and test images.

## Requirements
### Python Packages
To use our software, you'll need to install several python packages. Please use `requirements.txt` to install the python packages:
```
pip install -r requirements.txt
```
### TensorFlow Object Detection API
Our detection framework is based on [TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection). So you need to install it before you use our program. We use the Object Detection API with TensorFlow 2.
Please find a detailed installation document [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2.md).



## Usage Example
### Quick Test
To have a quick test of the code, you can simplily run `python detect.py` in Terminal. The test image in `res/testimg/input/` will be anonymized and you can find the output image in `res/testimg/input/anonymized/`.

### Anonymize Your Images
If you want to anonymized your own images or use your own model, please follow the usage example.
```
    python detect.py \
        --model_car_person_dir=res/model/car_person/ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03/saved_model/ \
        --model_face_license_dir=res/model/face_license/face_license/saved_model/ \
        --threshold=0.2 \
        --detail=False\
        --input_dir=res/testimg/input/ \
        --output_dir=res/testimg/output/
```
* `model_car_person_dir` This directory contains the model for car and person detection. There should be a *.pb model in this directory.
* `model_face_license_dir` This directory contains the model for human face and vehicle license plate detection. There should be a *.pb model in this directory.
* `threshold` Confidence threshold. It is recommended to set the confidence threshold between 0.2 ~ 0.3.
* `detail` If you set `detail` as `True`, the output of each important step will be saved. In `car_pereson/` you will find the detected vehicle and person. In `merged_box/` you will find all mereged box, which is the input of second model. In `face_license/` you will find the detected human face and license plate as well as confidence of each detected box. In `box_location/` you will find the box location saved as *.txt file. The data is organized in this format: `class confidence x_min y_min x_max y_max`.
* `input_dir` The directory of input images.
* `output_dir` The directory for saving anonymized images.
