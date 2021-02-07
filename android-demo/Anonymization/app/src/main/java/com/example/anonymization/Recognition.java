package com.example.anonymization;

import android.graphics.Rect;
import android.graphics.RectF;

public class Recognition {
    private String label;
    private RectF location;
    private float prob;

    private final Rect locationInt;
    private final int imgHeight;
    private final int imgWidth;

    public Recognition(String label, RectF location, float prob, int imgHeight, int imgWidth) {
        this.label = label;
        this.location = location;
        this.prob = prob;
        this.imgHeight = imgHeight;
        this.imgWidth = imgWidth;
        this.locationInt = new Rect(Math.round(location.left * imgWidth),
                Math.round(location.top * imgHeight),
                Math.round(location.right * imgWidth),
                Math.round(location.bottom * imgHeight));
    }

    public Rect getLocationInt() {
        return locationInt;
    }

    public int getImgHeight() {
        return imgHeight;
    }

    public int getImgWidth() {
        return imgWidth;
    }

    public String getLabel() {
        return label;
    }

    public RectF getLocation() {
        return location;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public void setLocation(RectF location) {
        this.location = location;
    }

    public void setProb(float prob) {
        this.prob = prob;
    }

    public float getProb() {
        return prob;
    }

    @Override
    public String toString() {
        return "Recognition{" +
                "label='" + label + '\'' +
                ", location=" + location +
                ", prob=" + prob +
                '}';
    }
}
