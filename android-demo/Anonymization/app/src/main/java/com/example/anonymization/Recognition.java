/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

package com.example.anonymization;

import android.graphics.Rect;
import android.graphics.RectF;

public class Recognition {
    private String label;
    private RectF location;
    private float prob;

    private Rect locationInt;
    private int imgHeight;
    private int imgWidth;

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
        this.locationInt = new Rect(Math.round(location.left * imgWidth),
                Math.round(location.top * imgHeight),
                Math.round(location.right * imgWidth),
                Math.round(location.bottom * imgHeight));
    }

    public void setLocationInt(Rect locationInt) {
        this.locationInt = locationInt;
        this.location = new RectF(locationInt.left / (float) imgWidth,
                locationInt.top / (float) imgHeight,
                locationInt.right / (float) imgWidth,
                locationInt.bottom / (float) imgHeight);
    }

    public void setProb(float prob) {
        this.prob = prob;
    }

    public float getProb() {
        return prob;
    }

    public void setImgHeight(int imgHeight) {
        this.imgHeight = imgHeight;
    }

    public void setImgWidth(int imgWidth) {
        this.imgWidth = imgWidth;
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
