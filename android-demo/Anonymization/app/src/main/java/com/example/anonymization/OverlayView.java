package com.example.anonymization;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;
import android.widget.ImageView;

import androidx.annotation.Nullable;

import java.util.List;

public class OverlayView extends androidx.appcompat.widget.AppCompatImageView {

    private List<Recognition> recognitions;

    private Paint borderPaint, textPaint;
    private static final int TEXT_SIZE = 24;
    private Bitmap framebitmap;

    public OverlayView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);

        borderPaint = new Paint();
        borderPaint.setColor(Color.RED);
        borderPaint.setStyle(Paint.Style.STROKE);
        borderPaint.setStrokeWidth(10.0f);

        textPaint = new Paint();
        textPaint.setColor(Color.RED);
        textPaint.setStyle(Paint.Style.FILL);
        textPaint.setTextSize(TEXT_SIZE);
    }

    public void setRecognitions(List<Recognition> recognitions) {
        this.recognitions = recognitions;
    }

    public void setFramebitmap(Bitmap bitmap){
        this.framebitmap = bitmap;
    }

    @Override
    public synchronized void draw(final Canvas canvas) {
        super.draw(canvas);
        if (recognitions != null) {
            Matrix frameToCanvasMatrix = getFrameToCanvasMatrix(canvas, framebitmap);

            for (Recognition r : recognitions) {
                frameToCanvasMatrix.mapRect(r.getLocation());
                float cornerSize = Math.min(r.getLocation().width(), r.getLocation().height()) / 8.0f;
                canvas.drawRoundRect(r.getLocation(), cornerSize, cornerSize, borderPaint);

                String labelString = String.format("%s %.2f%%", r.getLabel(), (100 * r.getProb()));
                canvas.drawText(
                        labelString,
                        r.getLocation().left + (int) 1.5 * TEXT_SIZE,
                        r.getLocation().top + (int) 1.5 * TEXT_SIZE,
                        textPaint
                );
            }
        }
    }

    private Matrix getFrameToCanvasMatrix(Canvas canvas, Bitmap bitmap) {
        int frameWidth = bitmap.getWidth();
        int frameHeight = bitmap.getHeight();
        int orientation = 0;

        boolean rotated = orientation % 180 == 90;
        float multiplier = Math.min(
                canvas.getHeight() / (float) (rotated ? frameWidth : frameHeight),
                canvas.getWidth() / (float) (rotated ? frameHeight : frameWidth)
        );

        return ImageUtils.getTransformationMatrix(
                frameWidth,
                frameHeight,
                (int) (multiplier * frameHeight),
                (int) (multiplier * frameWidth),
                orientation,
                false
        );
    }
}
