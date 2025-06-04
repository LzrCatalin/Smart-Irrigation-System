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
	
	logging.debug(Fore.WHITE + 
			  f"===INIT SETUP===\n\t Port: {port}"
			  +Style.RESET_ALL)
	
	i2c = busio.I2C(board.SCL, board.SDA)

	# ADC found at address 0x4a from I2C protocol
	ads = ADS.ADS1115(i2c, address = 0x48)

	# Check if sensor port from db is valid 
	if port in CHANNEL_MAPPING:

		# Get corresponding channel
		logging.debug(Fore.WHITE +
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
			   "\t<!>UNAVAILABLE<!>"
			   + Style.RESET_ALL)
		
		return None

#################################
#
#	Function to calculate soil
#	humidity percentage
#
#################################
def moisture_percentage(adc_value):

	# Calibrate based on actual sensor behavior
	dry_value = 26500  # ADC value for 0% humidity (dry)
	wet_value = 18900  # ADC value for 100% humidity (wet)

	# Clamp adc_value to [wet_value, dry_value]
	adc_value = max(min(adc_value, dry_value), wet_value)

	# Calculate percentage
	percentage = ((dry_value - adc_value) / (dry_value - wet_value)) * 100

	logging.info(Fore.LIGHTWHITE_EX 
			  + f"\tRetrieving moisture percentage: {percentage:.2f}%"
			  + Style.RESET_ALL)

	return percentage
