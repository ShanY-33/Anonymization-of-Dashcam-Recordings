# Android Sample Code

<img src="../img/android-demo.gif" width="50%">

## Use Other Model
If you want to use other model, please do the following steps:
* The .tflite model and label `labelmap1.txt` need to be located in `./Anonymization/app/src/main/assets/`. If you use COCO dataset label, then you don't need to change the labelmap file.
* According to the model structure, you need to make some minor changes in the code. More details are in the code comment.
    * ./Anonymization/app/src/main/java/com/example/anonymization/Imgprocess.java

        ```
        private static final int SCALE_SIZE1 = 300, SCALE_SIZE2 = 300;
        ```
        
    * ./Anonymization/app/src/main/java/com/example/anonymization/MainActivity.java

        ```
        private void gotoDetectionProcess(Bitmap bitmap){
            ...
            Detector detector1 = new Detector(this, "ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03.tflite", "labelmap1.txt", 0.3f, false);
            ...
        }
        ```
