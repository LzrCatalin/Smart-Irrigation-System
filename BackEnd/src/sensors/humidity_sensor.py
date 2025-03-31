import time
import board
import busio
import logging
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from src.services.sensors_services import *


#
#	Port config for ADS1115
#
CHANNEL_MAPPING = {
		0: ADS.P0,
		1: ADS.P1,
		2: ADS.P2,
		3: ADS.P3
	}

NOISE_THRESHOLD = 500

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
	ads = ADS.ADS1115(i2c, address = 0x48)

	# Check if sensor port from db is valid 
	if port in CHANNEL_MAPPING:

		# Get corresponding channel
		logging.info(Fore.WHITE +
			f"\tChannel: {CHANNEL_MAPPING[port]}"
			+ Style.RESET_ALL)
		
		channel = AnalogIn(ads, CHANNEL_MAPPING[port])
		adc_value = channel.value

		logging.debug(Fore.MAGENTA +
					f"Channel value: {adc_value}"
					+ Style.RESET_ALL)

		# Verify adc value based on threshold
		if adc_value < NOISE_THRESHOLD:
			logging.info(Fore.RED +
						f"\t<!> NO SENSOR CONNECTED <!>"
						+ Style.RESET_ALL)
			return None

		return channel.value


	else:
		logging.info(Fore.WHITE +
			   f"\t<!>UNAVAILABLE<!>"
			   + Style.RESET_ALL)
		
		return None

#################################
#
#	Function to calculate soil
#	humidity percentage
#
#################################
def moisture_percentage(adc_value):
	
	# MH Sensor-Series values configuration
	wet_value = 26330 # 100% soil humidity
	dry_value = 13330 # 0% soil humidity
	
	# TODO: Make more tests to find the best values for both ends
	percentage = (1 - ((adc_value - dry_value)/(wet_value - dry_value))) * 100

	logging.info(Fore.LIGHTWHITE_EX 
			  + f"\tRetrieving moisture percentage: {percentage:.2f}%"
			  + Style.RESET_ALL)
	
	return percentage
