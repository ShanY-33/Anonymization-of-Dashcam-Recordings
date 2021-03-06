package com.example.anonymization;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.RectF;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Imgprocess {

    private Bitmap frameBitmap;
    private int previewHeight, previewWidth;
    private Bitmap scaledBitmap;
    private Matrix frameToCropTransform;
    private Matrix cropToFrameTransform;
    private Matrix normToCropTransform;
    private Matrix cropToScaledCropTransform;

    private static final int SCALE_SIZE1 = 300, SCALE_SIZE2 = 300;

    private Detector detector1,detector2;
    private OverlayView overlayView;

    public Imgprocess(Bitmap bitmap, OverlayView overlayView, Detector detector1, Detector detector2){
        this.frameBitmap = bitmap;
        this.previewHeight = bitmap.getHeight();
        this.previewWidth = bitmap.getWidth();
        this.overlayView = overlayView;
        this.detector1 = detector1;
        this.detector2 = detector2;
        frameToCropTransform = ImageUtils.getTransformationMatrix(
                previewWidth,
                previewHeight,
                SCALE_SIZE1,
                SCALE_SIZE1,
                0,
                false
        );

        normToCropTransform = ImageUtils.getTransformationMatrix(
                1,
                1,
                SCALE_SIZE1,
                SCALE_SIZE1,
                0,
                false
        );

        cropToFrameTransform = new Matrix();
        frameToCropTransform.invert(cropToFrameTransform);

        scaledBitmap = Bitmap.createBitmap(SCALE_SIZE1, SCALE_SIZE1, Bitmap.Config.ARGB_8888);
    }

    private void ScaleImg(Bitmap srcBitmap, Bitmap dstBitmap, Matrix transformMatrix){
        Canvas canvas = new Canvas(dstBitmap);
        canvas.drawBitmap(srcBitmap, transformMatrix, null);
    }

    /**
     * @description This is the main detection process.
     */
    protected void detectprocess(){
        // scale the image to the required input size of model
        ScaleImg(frameBitmap, scaledBitmap, frameToCropTransform);

        // detect objects using detector1
        List<Recognition> recognitionList1 = detector1.detect(scaledBitmap,frameBitmap);
        // remove unnecessary detected recognitions
        String[] classes = {"person","car","bicycle","motorcycle","bus","truck"};
        recognitionList1 = ImageUtils.filteroutRecognitions(classes, recognitionList1);
        // merge the overlapped and adjacent recognitions
        recognitionList1 = ImageUtils.mergeRecognitions(this.previewHeight,this.previewWidth, recognitionList1);
        // expand the boundary of the recognitions
        recognitionList1 = ImageUtils.extendRecognitions(this.previewHeight,this.previewWidth,recognitionList1,10);

        // crop the detected person and vehicle from the original image
        List<Bitmap> cropedBitmapsList = new ArrayList<>();
        for (Recognition recognition:recognitionList1
             ) {
            cropedBitmapsList.add(ImageUtils.cropImg(frameBitmap, recognition));
        }

        // scale the image to the required input size of model
        List<Bitmap> scaledCropedBitmapsList = new ArrayList<>();
        for (Bitmap bitmap:cropedBitmapsList
             ) {
            cropToScaledCropTransform = ImageUtils.getTransformationMatrix(
                    bitmap.getWidth(),
                    bitmap.getHeight(),
                    SCALE_SIZE2,
                    SCALE_SIZE2,
                    0,
                    false
            );
            Bitmap scaledBitmap2 = Bitmap.createBitmap(SCALE_SIZE2, SCALE_SIZE2, Bitmap.Config.ARGB_8888);
            ScaleImg(bitmap, scaledBitmap2, cropToScaledCropTransform);
            scaledCropedBitmapsList.add(scaledBitmap2);
        }

        // detect with detector2 to detect human face and license plate
        List<List<Recognition>> recognitionListList = new ArrayList<>();
        for (int i = 0; i < scaledCropedBitmapsList.size(); i++) {
            recognitionListList.add(detector2.detect(scaledCropedBitmapsList.get(i), cropedBitmapsList.get(i)));
        }

        // calculate the location of recognitions in the original image, the final recogtions will be saved in recognitionList2
        List<Recognition> recognitionList2 = new ArrayList<>();
        for (int i = 0; i < recognitionListList.size(); i++) {
            for (int j = 0; j < recognitionListList.get(i).size(); j++) {
                Recognition tmpRecognition;
                tmpRecognition = ImageUtils.convertRecognitiontoOriginalImg(recognitionList1.get(i), recognitionListList.get(i).get(j));
                recognitionList2.add(tmpRecognition);
            }
        }

        System.out.println("Detection is finished");

        // convert recognition to scaledBitmap
        for(Recognition recognition : recognitionList2) {
            normToCropTransform.mapRect(recognition.getLocation());
        }

        // convert scaledBitmap to frameBitmap
        for(Recognition recognition : recognitionList2) {
            cropToFrameTransform.mapRect(recognition.getLocation());
        }

        overlayView.setRecognitions(recognitionList2);
        overlayView.setImageBitmap(frameBitmap);
        overlayView.postInvalidate();
    }


}
