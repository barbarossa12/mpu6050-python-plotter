#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);  // Wait for Serial on native USB

  // Initialize I2C
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  Serial.println("MPU6050 Found!");

  // Configure range and filters
  // sets the maximum range the accelerometer can measure
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  // sets the maximum range for the gyroscope
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  // sets the Digital LowPass Filter bandwidth. 
  // filters out the noise above 21Hz
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);
}

void loop() {
  sensors_event_t accel, gyro, temp;

  mpu.getEvent(&accel, &gyro, &temp);

  Serial.print("A:");
  Serial.print(accel.acceleration.x); Serial.print(",");
  Serial.print(accel.acceleration.y); Serial.print(",");
  Serial.print(accel.acceleration.z); Serial.print(";G:");
  Serial.print(gyro.gyro.x); Serial.print(",");
  Serial.print(gyro.gyro.y); Serial.print(",");
  Serial.println(gyro.gyro.z);

  delay(50);  // Match sample rate
}
