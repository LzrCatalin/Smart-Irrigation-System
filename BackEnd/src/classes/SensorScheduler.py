import atexit
from colorama import Fore
from flask_apscheduler import APScheduler
from src.services import sensors_services
from src.services import fields_service
from src.classes.Sensor import *
from src.classes.Field import *
from src.sensors.humidity_sensor import *
from src.sensors.temperature_sensor import *
from src.services.fields_service import get_fields_data, get_field_user
from src.util.utils import alert

####################
#
#   Scheduler configurations
#
####################
class SensorScheduler:
	def __init__(self, app, irrigation_system):
		self.scheduler = APScheduler()
		self.scheduler.init_app(app)
		self.scheduler.start()
		self.irrigation_system = irrigation_system

	def periodic_fields_sensor_update(self):
		"""Run periodic fields measurements"""
		
		logging.debug(Fore.MAGENTA +
				"\t <!> Starting Periodic Update <!>"
				+ Style.RESET_ALL)

		# Fetch fields ids
		fields_data = get_fields_data()

		for field_id, field_data in fields_data.items():
			if not field_data or not field_data['sensors']:
				continue

			# Initialize measurements
			new_humidity = None
			new_temperature = None
			new_port = None

			# Update field's sensors
			for sensor in field_data['sensors']:
				
				# Display each sensor data
				self.display_sensor_details(sensor)

				sensor_type = sensor['type']['type']
				sensor_port = sensor['type']['port']
				new_port = sensor_port

				if sensor_type == Type.HUMIDITY.name:
					adc_value = sensor_setup(sensor_port)

					if adc_value is not None:
						new_humidity = moisture_percentage(adc_value)
						sensor['type']['measured_value'] = new_humidity

				elif sensor_type == Type.TEMPERATURE.name:
					slave_file = sensor_file(sensor_port)

					if slave_file is not None:
						new_temperature = read_temperature(slave_file)
						sensor['type']['measured_value'] = new_temperature

			# Update field entity in the database
			if new_humidity is not None and new_temperature is not None:
				fields_service.update_field_measurements_by_id(field_id, Field.from_dict(field_data))

				# Update irrigation system management
				self.irrigation_system.add_field(field_id)
				self.irrigation_system.update_field_measurements(
					field_id= field_id,
					humidity=new_humidity if new_humidity is not None 
										else self.irrigation_system.fields[field_id].current_humidity,
					temperature=new_temperature if new_temperature is not None 
										else self.irrigation_system.fields[field_id].current_temperature,
					port=new_port					
										)
				
				# Check if the field's humidity is on a critical value
				self.irrigation_system.check_critical_humidity(field_id)
				
				# Send alert
				alert(
					user_id=get_field_user(field_id),
					message=f"Crop {field_data['crop_name']} system measurements updated."
				)

	def schedule_sensor_updates(self, interval: int):
		"""Schedule automatic updates on sensors cycle"""
		if not self.scheduler.get_job('sensor_update_cycle'):
			self.scheduler.add_job(
				id='sensor_update_cycle', 
				func=self.periodic_fields_sensor_update,
				trigger = 'interval', 
				seconds = interval
			)
			logging.info(f'Scheduled sensors updates cycles every {interval} seconds')

	def get_schedules(self):
		print(self.scheduler.get_jobs())

	def display_sensor_details(self, sensor_data: dict) -> None:
		logging.debug(Fore.MAGENTA +
			f"Port: {sensor_data['type']['port']}"
			+ Style.RESET_ALL)
		
		logging.debug(Fore.MAGENTA +
			f"Type: {sensor_data['type']['type']}"
			+ Style.RESET_ALL)
		
		logging.debug(Fore.MAGENTA +
			f"Status: {sensor_data['type']['status']}"
			+ Style.RESET_ALL)

	def start(self):
		"""Turn ON the scheduler"""
		if not self.scheduler.running:
			logging.info('Turn ON sensor scheduler...')
			self.scheduler.start()

		else:
			logging.info('Sensor scheduler is already running')

	def stop(self):
		"""Stop the scheduler"""
		if self.scheduler.running:
			logging.info('Stoping sensor scheduler...')
			self.scheduler.shutdown()

		else:
			logging.info('Sensor scheduler is already stopped')

	def pause_sensor_updates(self):
		"""Pause the periodic sensor update job"""
		job = self.scheduler.get_job('sensor_update_cycle')
		
		if job:
			job.pause()
			logging.info('Paused sensor updates')
		
		else:
			logging.warning('Sensor update job not found to pause')

	def resume_sensor_updates(self):
		"""Resume the periodic sensor update job"""
		job = self.scheduler.get_job('sensor_update_cycle')
		
		if job:
			job.resume()
			logging.info('Resumed sensor updates')
		
		else:
			logging.warning('Sensor update job not found to resume')

	def update_interval(self, new_interval: int) -> None:
		"""Update scheduler time interval"""
		job = self.scheduler.get_job('sensor_update_cycle')

		if job:
			self.scheduler.scheduler.reschedule_job(
				job_id='sensor_update_cycle',
				trigger='interval',
				seconds=new_interval
			)
			logging.info(f'Sensor updates timer updated to run every {new_interval} seconds')
		
		else:
			logging.warning('Sensor update job not found to update interval')

	def scheduler_shutdown(self):
		atexit.register(self.stop)