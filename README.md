# Anonymization of Dashcam Recordings

## Introduction
In order to be able to use these images in research projects without hesitation, they should be made compliant with data protection laws. Faces as well as vehicle registration plates are to be made unrecognizable for this purpose.

## Architecture
The repository is split up into these directories:

* `python-demo/` python code for anonymization
* `orga/` slides of each milestone and final paper
* `model/` trained SSD Mobilenet model

For more information about each directory, its contents and its functions, please consult the corresponding readme found in each directory.

## Approach
The code follows the steps given below:
* Read the images from a directory.
* Use the first model to detect all objects in the image.
* According the label we can filter out the classes that we need, i.e. vehicle and person.
* Merge the overlapped and adjacent boxes.
* Feed each merged boxes to the second model for detection of human faces and license plates.
* Calculate the detected boxes position in the original image.
* Blur the correspond area.





## Results
<img src="overview-arch.jpg" width="100%">
<img src="overview-arch.jpg" width="100%">
<img src="overview-arch.jpg" width="100%">
You can find project report [here](./UserGuide.md).


