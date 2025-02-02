/**
 * Detector is based on: ObjectDetectorTutorial
 * https://github.com/William-Yin123/ObjectDetector
 */

package com.example.anonymization;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Rect;
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
    public final String MODEL_PATH;
    public final String LABEL_PATH;
    private final float THRESHOLD;
    private static final float IMAGE_MEAN = 127.5f;
    private static final float IMAGE_STD = 127.5f;
    private static final int NUM_DETECTIONS = 10;

    private final Interpreter tflite;
    private final int imageSizeX;
    private final int imageSizeY;
    private List<String> labels;
    boolean quantized;

    /**
     * Constructor
     * @param context
     * @param MODEL_PATH file name of the model
     * @param LABEL_PATH
     * @param THRESHOLD threshold of confidence
     * @param quantized If the model is a quantized model,set it true. Else if it is a float model, set it false
     */
    public Detector(Context context, String MODEL_PATH, String LABEL_PATH, float THRESHOLD, boolean quantized) {
        try {
            this.MODEL_PATH = MODEL_PATH;
            this.LABEL_PATH = LABEL_PATH;
            this.THRESHOLD = THRESHOLD;
            this.quantized = quantized;
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

    public List<Recognition> detect(Bitmap bitmap, Bitmap originalImg) {
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

        int numBytesPerChannel;
        // different value depends on whether the tflite model is quantized or not
        if (this.quantized) numBytesPerChannel = 1;
        else numBytesPerChannel = 4;

        ByteBuffer imgData = ByteBuffer.allocateDirect(
                1 * imageSizeX * imageSizeY * 3 * numBytesPerChannel);
        imgData.order(ByteOrder.nativeOrder());

        for (int i = 0; i < imageSizeY; i++) {
            for (int j = 0; j < imageSizeX; j++) {
                int pixelValue = intValues[i * imageSizeX + j];

                // different operation depends on whether the tflite model is quantized or not
                if (this.quantized) {
                    imgData.put((byte) ((pixelValue >> 16) & 0xFF));
                    imgData.put((byte) ((pixelValue >> 8) & 0xFF));
                    imgData.put((byte) (pixelValue & 0xFF));
                } else {
                    imgData.putFloat((((pixelValue >> 16) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                    imgData.putFloat((((pixelValue >> 8) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                    imgData.putFloat(((pixelValue & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                }
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

        // get runtime of each detection
//        long timeStamp0 = System.currentTimeMillis();

        tflite.runForMultipleInputsOutputs(inputArray, outputMap);

//        long timeStamp1 = System.currentTimeMillis();
//        long time = timeStamp1 - timeStamp0;
//        Log.d("detection time cost", " "+time+" ms");


        List<Recognition> recognitions = new ArrayList<>();
        for (int i = 0; i < numDetections[0]; i++) {
            float prob = outputScores[0][i];
            if (prob > this.THRESHOLD) {
                String label = labels.get((int) outputClasses[0][i] + 1);
                RectF location = new RectF(
                        outputLocations[0][i][1] * 1,
                        outputLocations[0][i][0] * 1,
                        outputLocations[0][i][3] * 1,
                        outputLocations[0][i][2] * 1
                );
                recognitions.add(new Recognition(label, location, prob, originalImg.getHeight(), originalImg.getWidth()));
            }
        }

        return recognitions;
    }

}
