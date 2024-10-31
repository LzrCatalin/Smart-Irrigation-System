import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#################################
#
#	Setup
#
#################################
def sensor_setup(port):
	i2c = busio.I2C(board.SCL, board.SDA)

	# ADC found at address 0x4a from I2C protocol
	ads = ADS.ADS1115(i2c, address = 0x4a)

	# Sensor AO connected to A0 port of ADS1115
	channel_mapping = {
		0: ADS.P0,
		1: ADS.P1,
		2: ADS.P2,
		3: ADS.P3
	}

	# Check if sensor port from db is valid 
	if port in channel_mapping:
		# Get corresponding channel
		channel = AnalogIn(ads, channel_mapping[port])
		return channel.value
	
#################################
#
#	Functio to calculate soil
#	humidity percentage
#
#################################
def calculate_moisture_percentage(adc_value):
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
def start():
	print("Turn ON soil measurements...")
	return calculate_moisture_percentage(adc_value)

#################################
#
#	Stop Measurements
#
#################################
def stop():
	print("Turning OFF soil measurements...")

#try:
#    while True:
#        adc_value = channel.value
#        print(f"ADC Value: {adc_value}")
#        
#        moisture_percentage = calculate_moisture_percentage(adc_value)
#        print(f"Soil moisture: {moisture_percentage:.2f}%")
#        
#        time.sleep(2)
		
#except KeyboardInterrupt:
#    print("Exiting...")