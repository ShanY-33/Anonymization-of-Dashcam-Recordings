package com.example.anonymization;

import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.graphics.Rect;
import android.util.Size;

import java.util.List;

public class ImageUtils {

    static final int kMaxChannelValue = 262143;

    public static int getYUVByteSize(Size size) {
        final int ySize = size.getWidth() * size.getHeight();
        final int uvSize = ((size.getWidth() + 1) / 2) * ((size.getHeight() + 1) / 2) * 2;

        return ySize + uvSize;
    }

    public static Matrix getTransformationMatrix(
            final int srcWidth,
            final int srcHeight,
            final int dstWidth,
            final int dstHeight,
            final int applyRotation,
            final boolean maintainAspectRatio) {
        final Matrix matrix = new Matrix();

        if (applyRotation != 0) {

            // Translate so center of image is at origin.
            matrix.postTranslate(-srcWidth / 2.0f, -srcHeight / 2.0f);

            // Rotate around origin.
            matrix.postRotate(applyRotation);
        }

        // Account for the already applied rotation, if any, and then determine how
        // much scaling is needed for each axis.
        final boolean transpose = (Math.abs(applyRotation) + 90) % 180 == 0;

        final int inWidth = transpose ? srcHeight : srcWidth;
        final int inHeight = transpose ? srcWidth : srcHeight;

        // Apply scaling if necessary.
        if (inWidth != dstWidth || inHeight != dstHeight) {
            final float scaleFactorX = dstWidth / (float) inWidth;
            final float scaleFactorY = dstHeight / (float) inHeight;

            if (maintainAspectRatio) {
                // Scale by minimum factor so that dst is filled completely while
                // maintaining the aspect ratio. Some image may fall off the edge.
                final float scaleFactor = Math.max(scaleFactorX, scaleFactorY);
                matrix.postScale(scaleFactor, scaleFactor);
            } else {
                // Scale exactly to fill dst from src.
                matrix.postScale(scaleFactorX, scaleFactorY);
            }
        }

        if (applyRotation != 0) {
            // Translate back from origin centered reference to destination frame.
            matrix.postTranslate(dstWidth / 2.0f, dstHeight / 2.0f);
        }

        return matrix;
    }

    public static void convertYUV420SPToARGB8888(byte[] input, int width, int height, int[] output) {
        final int frameSize = width * height;
        for (int j = 0, yp = 0; j < height; j++) {
            int uvp = frameSize + (j >> 1) * width;
            int u = 0;
            int v = 0;

            for (int i = 0; i < width; i++, yp++) {
                int y = 0xff & input[yp];
                if ((i & 1) == 0) {
                    v = 0xff & input[uvp++];
                    u = 0xff & input[uvp++];
                }

                output[yp] = YUV2RGB(y, u, v);
            }
        }
    }

    private static int YUV2RGB(int y, int u, int v) {
        // Adjust and check YUV values
        y = (y - 16) < 0 ? 0 : (y - 16);
        u -= 128;
        v -= 128;

        // This is the floating point equivalent. We do the conversion in integer
        // because some Android devices do not have floating point in hardware.
        // nR = (int)(1.164 * nY + 2.018 * nU);
        // nG = (int)(1.164 * nY - 0.813 * nV - 0.391 * nU);
        // nB = (int)(1.164 * nY + 1.596 * nV);
        int y1192 = 1192 * y;
        int r = (y1192 + 1634 * v);
        int g = (y1192 - 833 * v - 400 * u);
        int b = (y1192 + 2066 * u);

        // Clipping RGB values to be inside boundaries [ 0 , kMaxChannelValue ]
        r = r > kMaxChannelValue ? kMaxChannelValue : (r < 0 ? 0 : r);
        g = g > kMaxChannelValue ? kMaxChannelValue : (g < 0 ? 0 : g);
        b = b > kMaxChannelValue ? kMaxChannelValue : (b < 0 ? 0 : b);

        return 0xff000000 | ((r << 6) & 0xff0000) | ((g >> 2) & 0xff00) | ((b >> 10) & 0xff);
    }

    protected static Bitmap cropImg(Bitmap bitmap, Recognition recognition) {
        return Bitmap.createBitmap(bitmap, recognition.getLocation().left,
                recognition.getLocation().top,
                recognition.getLocation().right - recognition.getLocation().left,
                recognition.getLocation().bottom - recognition.getLocation().top);
    }

    protected static List<Recognition> mergeRecognition(Bitmap bitmap, List<Recognition> recognitionList){
        boolean flag = false;
        int left1, top1, right1, bottom1;
        int left2, top2, right2, bottom2;
        while (!flag){
            boolean ifModify = false;
            for (int i = recognitionList.size()-1; i >0 ; i--) {
                left1 = recognitionList.get(i).getLocation().left;
                top1 = recognitionList.get(i).getLocation().top;
                right1 = recognitionList.get(i).getLocation().right;
                bottom1 = recognitionList.get(i).getLocation().bottom;
                for (int j = i-1; j >0; j--){
                    left2 = recognitionList.get(j).getLocation().left;
                    top2 = recognitionList.get(j).getLocation().top;
                    right2 = recognitionList.get(j).getLocation().right;
                    bottom2 = recognitionList.get(j).getLocation().bottom;


                }


            }

        }

        return recognitionList;
    }

    private static float calculateIOU(Bitmap bitmap, Rect rect1, Rect rect2) {
        float IOU;
        int width1 = rect1.right - rect1.left, width2 = rect2.right - rect2.left;
        int height1 = rect1.bottom - rect1.top, height2 = rect2.bottom - rect2.top;


        return IOU;
    }

    private static boolean isNear(Bitmap bitmap, Rect rect1, Rect rect2) {
        if (isSmall(bitmap, rect1) || isSmall(bitmap, rect2)) {
            boolean xNear = Math.abs((rect1.right + rect1.left) / 2.0 - (rect2.right + rect2.left) / 2.0)
                    < 0.1 * bitmap.getHeight() + (rect1.right - rect1.left) / 2.0 + (rect2.right - rect2.left) / 2.0;
            boolean yNear = Math.abs((rect1.bottom + rect1.top) / 2.0 - (rect2.bottom + rect2.top) / 2.0)
                    < 0.1 * bitmap.getHeight() + (rect1.bottom - rect1.top) / 2.0 + (rect2.bottom - rect2.top) / 2.0;
            if (xNear && yNear) return true;
        }
        return false;
    }

    private static boolean isSmall(Bitmap bitmap, Rect rect) {
        return ((rect.bottom - rect.top) < 0.1 * bitmap.getHeight()
                && (rect.right - rect.left) < 0.1 * bitmap.getWidth());
    }

}
