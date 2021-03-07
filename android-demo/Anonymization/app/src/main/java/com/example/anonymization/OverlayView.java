package com.example.anonymization;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.View;
import android.widget.ImageView;

import androidx.annotation.Nullable;

import java.util.List;

public class OverlayView extends androidx.appcompat.widget.AppCompatImageView {

    private List<Recognition> recognitions;

    private Paint borderPaint, textPaint;
    private static final int TEXT_SIZE = 24;
    private Bitmap frameBitmap;

    public OverlayView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);

        borderPaint = new Paint();
        borderPaint.setColor(Color.BLACK);
    }

    public void setRecognitions(List<Recognition> recognitions) {
        this.recognitions = recognitions;
    }

    public void setFramebitmap(Bitmap bitmap){
        this.frameBitmap = bitmap;
    }

    @Override
    public synchronized void draw(final Canvas canvas) {
        super.draw(canvas);
        if (recognitions != null) {
            Matrix frameToCanvasMatrix = getFrameToCanvasMatrix(canvas, frameBitmap);

            for (Recognition r : recognitions) {
                frameToCanvasMatrix.mapRect(r.getLocation());
                float cornerSize = Math.min(r.getLocation().width(), r.getLocation().height()) / 8.0f;
                canvas.drawRoundRect(r.getLocation(), cornerSize, cornerSize, borderPaint);

                //Draw Label Text
                /*
                String labelString = String.format("%s %.2f%%", r.getLabel(), (100 * r.getProb()));
                canvas.drawText(
                        labelString,
                        r.getLocation().left + (int) 1.5 * TEXT_SIZE,
                        r.getLocation().top + (int) 1.5 * TEXT_SIZE,
                        textPaint
                );
                */
            }
        }
    }

    private Matrix getFrameToCanvasMatrix(Canvas canvas, Bitmap bitmap) {
        int frameWidth = bitmap.getWidth();
        int frameHeight = bitmap.getHeight();

        float multiplierW = canvas.getWidth()/(float) frameWidth;
        float multiplierH = canvas.getHeight()/(float) frameHeight;

        return ImageUtils.getTransformationMatrix(
                frameWidth,
                frameHeight,
                (int) (multiplierW * frameWidth),
                (int) (multiplierH * frameHeight),
                0,
                false
        );
    }
}
