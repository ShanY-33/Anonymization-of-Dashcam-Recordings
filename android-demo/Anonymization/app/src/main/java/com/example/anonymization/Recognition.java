package com.example.anonymization;

import android.graphics.Rect;

public class Recognition {
    private String label;
    private Rect location;
    private float prob;

    public Recognition(String label, Rect location, float prob) {
        this.label = label;
        this.location = location;
        this.prob = prob;
    }

    public String getLabel() {
        return label;
    }

    public Rect getLocation() {
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
