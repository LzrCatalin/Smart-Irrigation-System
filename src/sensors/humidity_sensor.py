import time
import board
import busio
import logging
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from src.services.sensors_services import *

#################################
#
#	Initialize Sensors from DB
#
#################################
def sensors_init():
    logging.info("\t\tSENSORS INITIALIZATION")

    # Fetch sensors data from db
    sensors_data = get_sensors_data()
    print(sensors_data)

    sensors = {}
    #
    #	Iterate through each sensors
    #
    for sensor in sensors_data:
        if sensor is None:
            continue
        
        print(sensor["id"])
        # Get sensor port
        # port = sensor.get("ports")
        # print(port)

        # if port is not None:
        #     # Fetch adc_value from sensor's port
        #     adc_value = sensor_setup(port)

        #     #
        #     # Append value to sensors map:
        #     #       Map that helps us to track initial 
        #     #       data sent by the sensor
        #     #
        #     if adc_value is not None:
        #         sensors[sensor["id"]] = calculate_moisture_percentage(adc_value)

        # else:
        #     print("Port unavailable.")
                 
    print(sensors)
    # Print available sensors
    print("Available sensors with initial value.")
    for id, moisture in sensors.items():
        print(f"Sensor id: {id}\tMoisture: {moisture:.2f}%")

#################################
#
#	Setup Sensor to ADC Port
#
#################################
def sensor_setup(port):
    print(f"Starting setup for sensor with port: {port}")
    i2c = busio.I2C(board.SCL, board.SDA)

    # ADC found at address 0x4a from I2C protocol
    ads = ADS.ADS1115(i2c, address = 0x4a)

    # Configuration of sensors port for ADS1115 
    channel_mapping = {
        0: ADS.P0,
        1: ADS.P1,
        2: ADS.P2,
        3: ADS.P3
    }

    # Check if sensor port from db is valid 
    if port in channel_mapping:
        # Get corresponding channel
        print(f"Channel mapping: {channel_mapping[port]} for sensor port: {port}")
        channel = AnalogIn(ads, channel_mapping[port])
        return channel.value
    
    else:
        print(f"Port not available.")
        return

#################################
#
#	Function to calculate soil
#	humidity percentage
#
#################################
def calculate_moisture_percentage(adc_value):
    logging.info("Calling moisture function ... ")
    
    # MH Sensor-Series values configuration
    wet_value = 12000 # 100% soil humidity
    dry_value = 32767 # 0% soil humidity
    
    # TODO: Make more tests to find the best values for both ends
    percentage = (1 - ((adc_value - wet_value)/(dry_value - wet_value))) * 100
    print(f"Soil moisture: {percentage:.2f}%")
    
    return percentage

#################################
#
#	Start Measurements
#
#################################
def start_sensors_measurement():
    return sensors_init()

