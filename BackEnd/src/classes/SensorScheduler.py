import atexit
from colorama import Fore
from flask_apscheduler import APScheduler
from src.services import sensors_services
from src.classes.Sensor import *
from src.sensors.humidity_sensor import *
from src.sensors.temperature_sensor import *

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
					"Starting Periodic Update"
					+ Style.RESET_ALL)
			
			# Fetch all ids from Firebase
			sensor_ids = sensors_services.get_sensors_ids()
			logging.debug(Fore.MAGENTA +
					f"Available IDs: {sensor_ids}"
					+ Style.RESET_ALL)

			# Iterate through sensors ids
			for id in sensor_ids:
				# Retrieve sensor data based on id
				sensor_data = sensors_services.get_sensor_data_by_id(id)
				logging.debug(Fore.MAGENTA +
					f"ID: {id} ---> Data: {sensor_data}"
					+ Style.RESET_ALL)
				
				# Fetch sensor port and type
				port = sensor_data['type']['port']
				logging.debug(Fore.MAGENTA +
					f"Port: {port}"
					+ Style.RESET_ALL)
				
				type = sensor_data['type']['type']
				logging.debug(Fore.MAGENTA +
					f"Type: {type}"
					+ Style.RESET_ALL)
				
				status = sensor_data['type']['status']
				logging.debug(Fore.MAGENTA +
					f"Status: {status}"
					+ Style.RESET_ALL)
				
				#
				#	Updating only sensors that are displayed on the fields
				#
				if status == Status.AVAILABLE.name:
					logging.info(Fore.CYAN +
						f"\t\tSensor with id: {id} not in function." 
						+ Style.RESET_ALL)

					continue
				
				# Fetch adc_value based on port
				if port:
					logging.debug(Fore.MAGENTA +
						f"Start for port: {port}"
						+ Style.RESET_ALL)

					# Check sensor type
					if type == Type.HUMIDITY.name:
						# Fetch adc_value from sensor's port
						logging.debug(Fore.MAGENTA +
							"Moving to sensor_setupt function..."
							+ Style.RESET_ALL)
						adc_value = sensor_setup(port)

						#
						#	Update moisture value
						#
						if adc_value is not None:
							sensor_data['type']['measured_value'] = moisture_percentage(adc_value)

							# Convert sensor_data to Sensor object
							sensor = Sensor(
								name=sensor_data["name"],
								type=SensorType(
									type=sensor_data["type"]["type"],
									measured_value=sensor_data["type"]["measured_value"],
									status=sensor_data["type"]["status"],
									port=sensor_data["type"]["port"],
								),
							)
			
							# Insert new data into Firebase
							sensors_services.update_sensor_by_id(id, sensor)

					# elif type == Type.TEMPERATURE.name:
					# 	# Search slave file for sensor port
					# 	slave_file = sensor_file(port)

					# 	# Check if slave file exists
					# 	if slave_file is not None:
					# 		#
					# 		#	Update temperature value
					# 		#
					# 		sensor_data['type']['measured_value'] = read_temperature(slave_file)

					else:
						# Handle unknown type
						logging.info(Fore.WHITE + 
				   		f"Type: {type} unknown." +
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


