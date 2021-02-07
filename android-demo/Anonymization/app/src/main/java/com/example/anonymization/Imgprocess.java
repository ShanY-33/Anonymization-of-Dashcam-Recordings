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

    private static final int SCALE_SIZE = 640;

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
                SCALE_SIZE,
                SCALE_SIZE,
                0,
                false
        );

        normToCropTransform = ImageUtils.getTransformationMatrix(
                1,
                1,
                SCALE_SIZE,
                SCALE_SIZE,
                0,
                false
        );

        cropToFrameTransform = new Matrix();
        frameToCropTransform.invert(cropToFrameTransform);

        scaledBitmap = Bitmap.createBitmap(SCALE_SIZE, SCALE_SIZE, Bitmap.Config.ARGB_8888);
    }

    protected void ScaleImg(){
        Canvas canvas = new Canvas(scaledBitmap);
        canvas.drawBitmap(frameBitmap, frameToCropTransform, null);
    }

    protected void detectprocess(){
        overlayView.setImageBitmap(scaledBitmap);
        List<Recognition> recognitionList = detector1.detect(scaledBitmap,frameBitmap);
        String[] classes = {"person","car","bicycle","motorcycle","bus","truck"};
        recognitionList = ImageUtils.filteroutRecognitions(classes, recognitionList);
        recognitionList = ImageUtils.mergeRecognitions(this.previewHeight,this.previewWidth, recognitionList);
        recognitionList = ImageUtils.extendRecognitions(this.previewHeight,this.previewWidth,recognitionList);
        List<Bitmap> cropedBitmapsList = new ArrayList<>();
        for (Recognition recognition:recognitionList
             ) {
            cropedBitmapsList.add(ImageUtils.cropImg(frameBitmap, recognition));
        }



        System.out.println("Detection is finished");

        //Normolized to Scaled
        for(Recognition recognition : recognitionList) {
            normToCropTransform.mapRect(recognition.getLocation());
        }

        //Scaled to Frameimg
        for(Recognition recognition : recognitionList) {
            cropToFrameTransform.mapRect(recognition.getLocation());
        }

        overlayView.setRecognitions(recognitionList);
        overlayView.postInvalidate();
    }


}
