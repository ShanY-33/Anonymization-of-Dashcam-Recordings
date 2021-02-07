package com.example.anonymization;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.RectF;

import java.util.List;

public class Imgprocess {

    private Bitmap frameBitmap;
    private Bitmap scaledBitmap;
    private Matrix frameToCropTransform;
    private Matrix cropToFrameTransform;
    private Matrix normToCropTransform;
    private int previewHeight, previewWidth;
    private static final int SCALE_SIZE = 640;

    private Detector detector;
    private OverlayView overlayView;

    public Imgprocess(Bitmap bitmap, OverlayView overlayView, Detector detector){
        this.frameBitmap = bitmap;
        this.previewHeight = bitmap.getHeight();
        this.previewWidth = bitmap.getWidth();
        this.overlayView = overlayView;
        this.detector = detector;
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
        List<Recognition> recognitionList = detector.detect(scaledBitmap);
//        recognitionList = ImageUtils.mergeRecognitions(this.frameBitmap, recognitionList);
//        recognitionList = ImageUtils.extendRecognitions(this.frameBitmap,recognitionList);

        System.out.println("Detection is finished");
        /*
        //Normolized to Scaled
        for(Recognition recognition : recognitions) {
            normToCropTransform.mapRect(recognition.getLocation());
        }*/
        //Scaled to Frameimg
        for(Recognition recognition : recognitionList) {
            cropToFrameTransform.mapRect(recognition.getLocation());
        }

        overlayView.setRecognitions(recognitionList);
        overlayView.postInvalidate();
    }


}
