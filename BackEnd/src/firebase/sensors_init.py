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

	if not sensors_data:
		logging.warning("No sensors data available in database.")
		return None
	
	humidity_sensors = {}
	temperature_sensors = {}

	#
	#	Iterate through sensors
	#
	for sensor_id, sensor_dict in sensors_data.items():
		
		if not sensor_dict:
			logging.warning(f"Sensor data for ID {sensor_id} is empty or invalid")
			continue

		sensor = Sensor.from_dict(sensor_dict)
		logging.info(f"Sensor: {sensor.to_dict()}")

		# Retrieve sensor port
		sensor_port = sensor.type.port
		logging.debug(f'\tSensor Port: {sensor_port}')
		sensor_type = sensor.type.type

		if sensor_port >= 0:
			logging.debug(f'\tStarting for port: {sensor_port}')
			# Check sensor type
			if sensor_type == Type.HUMIDITY.name:
				# Fetch adc_value from sensor's port
				adc_value = sensor_setup(sensor_port)

				#
				# Append value to humidity sensors map:
				#       Track initial data sent by sensor
				#
				if adc_value is not None:
					humidity_sensors[sensor_id] = moisture_percentage(adc_value)

				else:
					logging.warning(f"Sensor ID {sensor_id} is not connected or invalid.")

			# elif type == Type.TEMPERATURE.name:
			# 	# Search slave file for sensor port
			# 	slave_file = sensor_file(port)

			# 	# Check if slave file exists
			# 	if slave_file is not None:
			# 		# Append value to temperature sensors map
			# 		temperature_sensors[sensorDTO.id] = read_temperature(slave_file)
		
		else:
			logging.debug(f'Fail to start for port: {sensor_port}')

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
	
	else:
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
	
	else:
		for id, temperature in temperature_sensors.items():
			print(f"\tSensor id: {id}\tTemperature: {temperature:.1f}C")