package de.hstr.ds.camel;

public class Measurement {
    String timestamp;
    String machineId;
    Sensor sensor;
    float value;

    public boolean isWarning() {
        switch (sensor) {
            case PRESSURE:
                return value > 5;
            case TEMPERATURE:
                return value > 50;
            default:
                return false;
        }
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getMachineId() {
        return machineId;
    }

    public void setMachineId(String machineId) {
        this.machineId = machineId;
    }

    public String getSensor() {
        return sensor.toString().toLowerCase();
    }

    public void setSensor(String sensor) {
        this.sensor = Sensor.valueOf(sensor.toUpperCase());
    }

    public float getValue() {
        return value;
    }

    public void setValue(float value) {
        this.value = value;
    }

    public String toString() {
        return String.format("{ \"timestamp\": \"%s\", \"machineId\": \"%s\", \"sensor\": \"%s\", \"value\": %.1f }",
                getTimestamp(), getMachineId(), getSensor(), getValue());
    }

    enum Sensor {
        TEMPERATURE, PRESSURE
    }
}
