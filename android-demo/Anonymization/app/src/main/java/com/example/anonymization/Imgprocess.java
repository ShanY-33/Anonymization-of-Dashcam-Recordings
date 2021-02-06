package com.example.anonymization;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;

import java.util.List;

public class Imgprocess {

    private Bitmap frameBitmap;
    private Bitmap scaledBitmap;
    private Matrix frameToCropTransform;
    private Matrix cropToFrameTransform;
    private int previewHeight, previewWidth;
    private static final int SCALE_SIZE = 300;

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
        List<Recognition> recognitions = detector.detect(scaledBitmap);
        System.out.println("Detection is finished");
        for(Recognition recognition : recognitions) {
            cropToFrameTransform.mapRect(recognition.getLocation());
        }

        overlayView.setRecognitions(recognitions);
        overlayView.postInvalidate();
    }

    protected Bitmap CropImg(Bitmap bitmap, Recognition recognition) {
        int imageSizeX = bitmap.getWidth(), imageSizeY = bitmap.getHeight();
        int left = Math.round(recognition.getLocation().left * imageSizeX);
        int top = Math.round(recognition.getLocation().top * imageSizeY);
        int right = Math.round(recognition.getLocation().right * imageSizeX);
        int bottom = Math.round(recognition.getLocation().bottom * imageSizeY);
        return (Bitmap.createBitmap(bitmap, left, top, right - left, bottom - top));
    }
}
