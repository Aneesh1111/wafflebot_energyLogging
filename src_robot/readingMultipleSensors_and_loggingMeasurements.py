from time import sleep
import board
import busio
import adafruit_tca9548a
import adafruit_ina219
import sys
import logging

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

# initialise logging sensor data
logging.basicConfig(
    filename='multiple_sensors.log', 
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )
logging.debug('Started')
print("running...")

# Read and print sensor data
while(1):
    # Initialize a list to store INA219 objects
    ina_sensors = []

    # Initialize INA219 sensors connected to each channel of the multiplexer
    for channel_number in range(num_channels):
        mux_channel = multiplexer[channel_number]
        ina_sensor = adafruit_ina219.INA219(mux_channel)
        ina_sensors.append(ina_sensor)
        name = channel_names.get(channel_number, "Channel " + str(channel_number))
        
        # logging data in a file
        logging.debug("{}: {:.2f} mW   ".format(name, ina_sensor.power * 1000))





