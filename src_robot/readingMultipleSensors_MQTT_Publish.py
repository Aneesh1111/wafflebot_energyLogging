#!/usr/bin/env python3

from time import sleep
import random
import paho.mqtt.client as mqtt
import board
import busio
import adafruit_tca9548a
import adafruit_ina219

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

broker = 'localhost'
# broker = 'broker.emqx.io'
client = mqtt.Client()
client.on_connect = on_connect 
client.connect(broker, port=1883, keepalive=60)

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize TCA9548A multiplexer on the I2C bus
multiplexer = adafruit_tca9548a.TCA9548A(i2c)

# Define the number of channels connected to the I2C multiplexer
num_channels = 7

# Define names for each channel
channel_names = {
    0: "PI",
    1: "Motor Left",
    2: "Motor Right",
    3: "Lidar",
    4: "Lidar Motor",
    5: "Battery",
    6: "USB"
}

# Read and print sensor data
while(1):
    # Initialize a list to store INA219 objects
    ina_sensors = []
    message = ""

    # Initialize INA219 sensors connected to each channel of the multiplexer
    for channel_number in range(num_channels):
        mux_channel = multiplexer[channel_number]
        ina_sensor = adafruit_ina219.INA219(mux_channel)
        ina_sensors.append(ina_sensor)

    # Read data from each sensor
    for channel_number, ina_sensor in enumerate(ina_sensors):
        name = channel_names.get(channel_number, "Channel " + str(channel_number))
        message += "{}: {:.2f} mW   ".format(name, ina_sensor.power * 1000)  # Power is in mW

    # Publish the power readings
    client.publish("topic/power_readings", message)
    print(f"send " + message + " to raspberry/topic")



