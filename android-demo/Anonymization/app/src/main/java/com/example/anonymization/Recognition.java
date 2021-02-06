package com.example.anonymization;

import android.graphics.RectF;

public class Recognition {
    private String label;
    private RectF location;
    private float prob;

    public Recognition(String label, RectF location, float prob) {
        this.label = label;
        this.location = location;
        this.prob = prob;
    }

    public String getLabel() {
        return label;
    }

    public RectF getLocation() {
        return location;
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
