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
    //private Bitmap scaledBitmap2;
    private Matrix frameToCropTransform;
    private Matrix cropToFrameTransform;
    private Matrix normToCropTransform;
    private Matrix cropToScaledCropTransform;

    private static final int SCALE_SIZE1 = 640, SCALE_SIZE2 = 300;

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
        //scaledBitmap2 = Bitmap.createBitmap(SCALE_SIZE2, SCALE_SIZE2, Bitmap.Config.ARGB_8888);
    }

    private void ScaleImg(Bitmap srcBitmap, Bitmap dstBitmap, Matrix transformMatrix){
        Canvas canvas = new Canvas(dstBitmap);
        canvas.drawBitmap(srcBitmap, transformMatrix, null);
    }

    protected void detectprocess(){
        ScaleImg(frameBitmap, scaledBitmap, frameToCropTransform);
        List<Recognition> recognitionList1 = detector1.detect(scaledBitmap,frameBitmap);

        String[] classes = {"person","car","bicycle","motorcycle","bus","truck"};
        recognitionList1 = ImageUtils.filteroutRecognitions(classes, recognitionList1);
        recognitionList1 = ImageUtils.mergeRecognitions(this.previewHeight,this.previewWidth, recognitionList1);
        recognitionList1 = ImageUtils.extendRecognitions(this.previewHeight,this.previewWidth,recognitionList1,10);

        List<Bitmap> cropedBitmapsList = new ArrayList<>();
        for (Recognition recognition:recognitionList1
             ) {
            cropedBitmapsList.add(ImageUtils.cropImg(frameBitmap, recognition));
        }

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
        //overlayView.setImageBitmap(scaledCropedBitmapsList.get(1));

        List<List<Recognition>> recognitionListList = new ArrayList<>();
        for (int i = 0; i < scaledCropedBitmapsList.size(); i++) {
            recognitionListList.add(detector2.detect(scaledCropedBitmapsList.get(i), cropedBitmapsList.get(i)));
        }

        List<Recognition> recognitionList2 = new ArrayList<>();
        for (int i = 0; i < recognitionListList.size(); i++) {
            for (int j = 0; j < recognitionListList.get(i).size(); j++) {
                Recognition tmpRecognition;
                tmpRecognition = ImageUtils.convertRecognitiontoOriginalImg(recognitionList1.get(i), recognitionListList.get(i).get(j));
                recognitionList2.add(tmpRecognition);
            }
        }


        System.out.println("Detection is finished");


        //Normolized to Scaled
        for(Recognition recognition : recognitionList2) {
            normToCropTransform.mapRect(recognition.getLocation());
        }

        //Scaled to Frameimg
        for(Recognition recognition : recognitionList2) {
            cropToFrameTransform.mapRect(recognition.getLocation());
        }

        overlayView.setRecognitions(recognitionList2);
        overlayView.setImageBitmap(frameBitmap);
        overlayView.postInvalidate();
    }


}
