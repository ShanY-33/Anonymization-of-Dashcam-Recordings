package com.example.anonymization;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.RectF;
import android.util.Log;

import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.support.common.FileUtil;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Detector {
    public static final String MODEL_PATH = "detect.tflite";
    public static final String LABEL_PATH = "labelmap.txt";
    private static final float IMAGE_MEAN = 127.5f;
    private static final float IMAGE_STD = 127.5f;
    private static final int NUM_DETECTIONS = 10;

    private final Interpreter tflite;
    private final int imageSizeX;
    private final int imageSizeY;
    private List<String> labels;

    public Detector(Context context) {
        try {
            labels = FileUtil.loadLabels(context, LABEL_PATH);
            tflite = new Interpreter(FileUtil.loadMappedFile(context, MODEL_PATH));

            int imageTensorIndex = 0;
            int[] imageShape = tflite.getInputTensor(imageTensorIndex).shape();
            imageSizeX = imageShape[2];
            imageSizeY = imageShape[1];

        } catch (IOException e) {
            Log.e(MainActivity.TAG, "Failed to load model from " + MODEL_PATH);
            throw new RuntimeException(e);
        }
    }

    public List<Recognition> detect(Bitmap bitmap) {
        int[] intValues = new int[imageSizeX * imageSizeY];
        bitmap.getPixels(
                intValues,
                0,
                bitmap.getWidth(),
                0,
                0,
                bitmap.getWidth(),
                bitmap.getHeight()
        );

        int numBytesPerChannel = 4;
        ByteBuffer imgData = ByteBuffer.allocateDirect(
                1 * imageSizeX * imageSizeY * 3 * numBytesPerChannel);
        imgData.order(ByteOrder.nativeOrder());

        for (int i = 0; i < imageSizeY; i++) {
            for (int j = 0; j < imageSizeX; j++) {
                int pixelValue = intValues[i * imageSizeX + j];
                /*
                imgData.put((byte) ((pixelValue >> 16) & 0xFF));
                imgData.put((byte) ((pixelValue >> 8) & 0xFF));
                imgData.put((byte) (pixelValue & 0xFF));*/
                imgData.putFloat((((pixelValue >> 16) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                imgData.putFloat((((pixelValue >> 8) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                imgData.putFloat(((pixelValue & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
            }
        }

        float[][][] outputLocations = new float[1][NUM_DETECTIONS][4];
        float[][] outputClasses = new float[1][NUM_DETECTIONS];
        float[][] outputScores = new float[1][NUM_DETECTIONS];
        float[] numDetections = new float[1];

        Object[] inputArray = {imgData};
        Map<Integer, Object> outputMap = new HashMap<>();
        outputMap.put(0, outputLocations);
        outputMap.put(1, outputClasses);
        outputMap.put(2, outputScores);
        outputMap.put(3, numDetections);

        tflite.runForMultipleInputsOutputs(inputArray, outputMap);
        List<Recognition> recognitions = new ArrayList<>();
        for (int i = 0; i < numDetections[0]; i++) {
            float prob = outputScores[0][i];
            if (prob > 0.3) {
                String label = labels.get((int) outputClasses[0][i] + 1);
                System.out.println(label);
                RectF location = new RectF(
                        outputLocations[0][i][1] * imageSizeX,
                        outputLocations[0][i][0] * imageSizeY,
                        outputLocations[0][i][3] * imageSizeX,
                        outputLocations[0][i][2] * imageSizeY
                );
                recognitions.add(new Recognition(label, location, prob));
            }
        }

        return recognitions;
    }

}
