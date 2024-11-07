import atexit
from colorama import Fore
from flask_apscheduler import APScheduler
from src.services import sensors_services
from src.classes.Sensor import Sensor
from src.sensors.testFunctions import *
from src.sensors.humidity_sensor import *
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
			# Fetch all ids from Firebase
			sensor_ids = sensors_services.get_sensors_ids()

			# Iterate through sensors ids
			for id in sensor_ids:
				# Retrieve sensor data based on id
				sensor_data = sensors_services.get_sensor_data_by_id(id)
				
				# Fetch sensor port and type
				port = sensor_data['type']['port']
				type = sensor_data['type']['type']
				status = sensor_data['type']['status']
				
				# Measure only for sensors that are displayed on the field
				if status == Status.AVAILABLE.name:
					logging.info(Fore.CYAN +
					f"\t\tSensor with id: {id} not in function." 
					+ Style.RESET_ALL)

					continue
				
				# Fetch adc_value based on port
				if port is not None:
					logging.info(Fore.LIGHTCYAN_EX +
				  	f"\t\tStart measuring for sensor id: {id}"
					+ Style.RESET_ALL)

					adc_value = sensor_setup(port)
					
					# Measure that based on sensor type
					if type == Type.HUMIDITY.name:
						sensor_data['type']['measured_value'] = calculate_moisture_percentage(adc_value)

					else:
						print("\t\tMeasuring for temperature sensor...")
						return 
					
					# Insert new data into Firebase
					sensors_services.update_sensor_by_id(id, sensor_data)

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


