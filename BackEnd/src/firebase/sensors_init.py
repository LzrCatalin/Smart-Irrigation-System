import logging

from src.services.sensors_services import *
from src.sensors.humidity_sensor import *
from src.sensors.temperature_sensor import *
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
	
	humidity_sensors = {}
	temperature_sensors = {}

	#
	#	Iterate through sensors
	#
	for sensor in sensors_data:
		if sensor is None:
			continue

		# Retrieve sensor port
		port = sensor['type']['port']
		type = sensor['type']['type']

		if port is not None:
			
			# Check sensor type
			if type == Type.HUMIDITY.name:
				# Fetch adc_value from sensor's port
				adc_value = sensor_setup(port)

				#
				# Append value to humidity sensors map:
				#       Track initial data sent by sensor
				#
				if adc_value is not None:
					humidity_sensors[sensor["id"]] = moisture_percentage(adc_value)

			elif type == Type.TEMPERATURE.name:
				# Search slave file for sensor port
				slave_file = sensor_file(port)

				# Check if slave file exists
				if slave_file is not None:
					# Append value to temperature sensors map
					temperature_sensors[sensor["id"]] = read_temperature(slave_file)

	# Print available sensors
	logging.info(Fore.WHITE + 
			  "=== DISPLAY AVAILABLE SENSORS INFORMATIONS ==="
			  +Style.RESET_ALL)
		
	logging.info(Fore.MAGENTA +
			   "\tHumidity Sensors"
			   + Style.RESET_ALL)
	
	#
	#	Verify if there are no humidity sensors
	#
	if not humidity_sensors:
		logging.info(Fore.LIGHTRED_EX +
			   "\tNo available sensors"
			   + Style.RESET_ALL)
	
	for id, moisture in humidity_sensors.items():
		print(f"\tSensor id: {id}\tMoisture: {moisture:.2f}%")

	logging.info(Fore.MAGENTA +
			   "\tTemperature Sensors"
			   + Style.RESET_ALL)
	
	#
	#	Verify if there are no temperature sensors
	#
	if not temperature_sensors:
		logging.info(Fore.LIGHTRED_EX +
			   "\tNo available sensors"
			   + Style.RESET_ALL)
		
	for id, temperature in temperature_sensors.items():
		print(f"\tSensor id: {id}\tTemperature: {temperature:.1f}C")