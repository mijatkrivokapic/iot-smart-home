#!/usr/bin/env python3
import MPU6050 
import time
import os

mpu = MPU6050.MPU6050()     #instantiate a MPU6050 class object
accel = [0]*3               #store accelerometer data
gyro = [0]*3                #store gyroscope data
def setup():
    mpu.dmp_initialize()    #initialize MPU6050
    
def run_gyro_sensor(delay, callback, stop_event, sensor_config=None):
    setup()
    while not stop_event.is_set():
        accel = mpu.get_acceleration()      #get accelerometer data
        gyro = mpu.get_rotation()           #get gyroscope data
        callback(accel, gyro, sensor_config)
        time.sleep(delay)


