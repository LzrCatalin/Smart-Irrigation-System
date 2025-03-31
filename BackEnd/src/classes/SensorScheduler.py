import atexit
from colorama import Fore
from flask_apscheduler import APScheduler
from src.services import sensors_services
from src.classes.Sensor import *
from src.classes.Field import *
from src.sensors.humidity_sensor import *
from src.sensors.temperature_sensor import *
from src.services import fields_service

####################
#
#   Scheduler configurations
#
####################
class SensorScheduler:
	def __init__(self, app):
		self.scheduler = APScheduler()
		self.scheduler.init_app(app)
		self.scheduler.start()
		

	def periodic_sensor_update(self):
			logging.debug(Fore.MAGENTA +
					"\t <!> Starting Periodic Update <!>"
					+ Style.RESET_ALL)
			
			# Fetch all ids from Firebase
			sensor_ids = sensors_services.get_sensors_ids()				

			# Start updating if exists any ids in db
			if sensor_ids:

				# Iterate through sensors ids
				for sensor_id in sensor_ids:
					# Retrieve sensor data based on id
					sensor_data = sensors_services.get_sensor_data_by_id(sensor_id)
					
					# Fetch sensor port , type and status
					sensor_port = sensor_data['type']['port']
					sensor_type = sensor_data['type']['type']
					sensor_status = sensor_data['type']['status']

					# Display details
					self.display_sensor_details(sensor_id, sensor_data)

					#
					#	Updating only sensors that are displayed on the fields
					#
					if sensor_status == Status.AVAILABLE.name:
						logging.info(Fore.CYAN +
								f"\t\tSensor with id: {id} not in function." 
									+ Style.RESET_ALL)

						continue
					
					# Fetch adc_value based on port
					if sensor_port >= 0:
						logging.debug(Fore.MAGENTA +
							f"Start for port: {sensor_port}"
							+ Style.RESET_ALL)

						# Check sensor type
						if sensor_type == Type.HUMIDITY.name:
							adc_value = sensor_setup(sensor_port)

							# Set new measured value
							if adc_value is not None:
								sensor_data['type']['measured_value'] = moisture_percentage(adc_value)

								# Call update function
								self.update(sensor_id, sensor_data, adc_value)

						elif sensor_type == Type.TEMPERATURE.name:
							# Search slave file for sensor port
							slave_file = sensor_file(sensor_port)

							# Check if slave file exists and set new measured value
							if slave_file is not None:
								sensor_data['type']['measured_value'] = read_temperature(slave_file)

								# Call update function
								self.update(sensor_id, sensor_data, slave_file)

						else:
							# Handle unknown type
							logging.info(Fore.WHITE + 
									f"Type: {type} unknown." +
										Style.RESET_ALL)
							break

			else:
				# No ids
				logging.info(Fore.LIGHTYELLOW_EX +
						f'No sensors in database.\n\tNo incoming updates.\n' +
						Style.RESET_ALL)



	def schedule_sensor_updates(self, duration):
		print(f"Sensor scheduler Turn ON for every {duration} seconds.")
		self.scheduler.add_job(id='sensor_update', 
						func=self.periodic_sensor_update,
						trigger = 'interval', 
						seconds = duration)


	def scheduler_shutdown(self):
		print("Sensors scheduler shutdown.")
		atexit.register(lambda: self.scheduler_shutdown())


	def get_schedules(self):
		print(self.scheduler.get_jobs())


	def update(self, sensor_id: str, sensor_data: dict, value: float | str) -> None:
		# Convert sensor_data to Sensor object
		updated_sensor = Sensor(
			name=sensor_data["name"],
			type=SensorType(
				type=sensor_data["type"]["type"],
				measured_value=sensor_data["type"]["measured_value"],
				status=sensor_data["type"]["status"],
				port=sensor_data["type"]["port"],
			),
			field_id=sensor_data.get("field_id")
		)


		# Retrieve field id from sensor data
		field_id = updated_sensor.field_id

		if field_id:
			# Fetch field based on id
			field = fields_service.get_field_by_id(field_id)

			if field:
				# Update the sensor in the field
				for sensor in field["sensors"]:
					if sensor["name"] == updated_sensor.name and sensor['type']['type'] == Type.HUMIDITY.name:
						sensor["type"]["measured_value"] = moisture_percentage(value)
						break

					if sensor["name"] == updated_sensor.name and sensor['type']['type'] == Type.TEMPERATURE.name:
						sensor["type"]["measured_value"] = read_temperature(value)
						break

		# Insert new data into Firebase
		sensors_services.update_sensor_by_id(sensor_id, updated_sensor)
		fields_service.update_field_measurements_by_id(field_id, Field.from_dict(field))


	def display_sensor_details(self, sensor_id: str, sensor_data: dict) -> None:
		logging.debug(Fore.MAGENTA +
		f"ID: {sensor_id} ---> Data: {sensor_data}"
		+ Style.RESET_ALL)
		
		logging.debug(Fore.MAGENTA +
			f"Port: {sensor_data['type']['port']}"
			+ Style.RESET_ALL)
		
		logging.debug(Fore.MAGENTA +
			f"Type: {sensor_data['type']['type']}"
			+ Style.RESET_ALL)
		
		logging.debug(Fore.MAGENTA +
			f"Status: {sensor_data['type']['status']}"
			+ Style.RESET_ALL)