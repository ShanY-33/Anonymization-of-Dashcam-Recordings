package com.shanshan.anonymizationproject.detection;

/**
 *
 */
public class Box {

    private float[] position;

    /**
     * @param position [xmin, ymin, xmax, ymax]
     */
    public Box(float[] position) {
        if (position.length == 4) {
            this.position = position;
        }
        else {
            throw new IllegalArgumentException("Illegal position!");
        }

    }

    public float[] getPosition() {
        return position;
    }

    public void setPosition(float[] position) {
        this.position = position;
    }
}
