import logging
from src.sensors.humidity_sensor import *
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

	# # Return sensors map
	# return sensors