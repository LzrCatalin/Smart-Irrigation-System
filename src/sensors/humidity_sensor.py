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

	if sensors_data is None:
		return None
	
	sensors = {}
	#
	#	Iterate through each sensors
	#
	for sensor in sensors_data:
		if sensor is None:
			continue

		# Retrieve sensor port
		port = sensor['type']['port']

		if port is not None:
			# Fetch adc_value from sensor's port
			adc_value = sensor_setup(port)

			#
			# Append value to sensors map:
			#       Track initial data sent by sensor
			#
			if adc_value is not None:
				sensors[sensor["id"]] = calculate_moisture_percentage(adc_value)

	# Print available sensors
	logging.info(Fore.WHITE + 
			  "=== DISPLAY AVAILABLE SENSORS INFORMATIONS ==="
			  +Style.RESET_ALL)
	
	for id, moisture in sensors.items():
		print(f"\tSensor id: {id}\tMoisture: {moisture:.2f}%")

#################################
#
#	Setup Sensor to ADC Port
#
#################################
def sensor_setup(port):
	logging.info(Fore.WHITE + 
			  f"===INIT SETUP===\n\t Port: {port}"
			  +Style.RESET_ALL)
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
		logging.info(Fore.WHITE +
			f"\tChannel: {channel_mapping[port]}"
			+ Style.RESET_ALL)
		
		channel = AnalogIn(ads, channel_mapping[port])
		return channel.value
	
	else:
		logging.info(Fore.WHITE +
			   f"\t<!>UNAVAILABLE<!>"
			   + Style.RESET_ALL)
		return

#################################
#
#	Function to calculate soil
#	humidity percentage
#
#################################
def calculate_moisture_percentage(adc_value):
	logging.info(Fore.WHITE
			  + f"Retrieving moisture humidity..."
			  + Style.RESET_ALL)
	
	# MH Sensor-Series values configuration
	wet_value = 12000 # 100% soil humidity
	dry_value = 32767 # 0% soil humidity
	
	# TODO: Make more tests to find the best values for both ends
	percentage = (1 - ((adc_value - wet_value)/(dry_value - wet_value))) * 100
	logging.info(Fore.BLUE 
			  + f"\t{percentage:.2f}%"
			  + Style.RESET_ALL)
	
	return percentage

#################################
#
#	Start Measurements
#
#################################
def start_sensors_measurement():
	return sensors_init()

