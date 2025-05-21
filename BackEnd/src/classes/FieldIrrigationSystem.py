import time
import logging

from typing import Dict
from flask_apscheduler import APScheduler
from src.classes.FieldIrrigation import FieldIrrigation

from src.services.users_service import get_user_ids
from src.services.fields_service import get_field_ids, get_field_user
from src.util.utils import alert

class FieldIrrigationSystem:
	"""Store fields that needs to be managed"""
	def __init__(self, app = None):
		self.fields: Dict[str, FieldIrrigation] = {}
		self.scheduler = APScheduler()
		self.scheduler.init_app(app)
		self.scheduler.start()
		self.sensors_scheduler = None

	def set_scheduler(self, scheduler) -> None:
		"""Set the scheduler of sensors"""
		self.sensors_scheduler = scheduler
	
	def system_init(self) -> None:
		"""Initialize system fields in case of a reset"""
		field_ids = get_field_ids()

		if field_ids:
			for id in field_ids:
				print(f"{id}")
				self.add_field(id)
			
			logging.info("System initialization completed.")

		else:
			logging.warning("Could not find any field ids found for init.")

	def add_field(self, field_id: str, config: dict = None) -> None:
		"""Add a new field to be managed"""
		if field_id not in self.fields:
			self.fields[field_id] = FieldIrrigation(field_id, config or {}, self.sensors_scheduler)
			logging.info(f"Field {field_id} added to system.")

	def remove_field(self, field_id: str) -> None:
		"""Remove data for a deleted field"""
		if field_id in self.fields:
			del self.fields[field_id]
			logging.info(f"Field {field_id} removed from the system.")

	def update_field_measurements(self, field_id: str, humidity: float, temperature: float, port: int) -> None:
		"""Update measurements of the field"""
		if field_id in self.fields:
			self.fields[field_id].current_humidity = humidity
			self.fields[field_id].current_temperature = temperature
			self.fields[field_id].current_port = port
			logging.info(f"Field {field_id} measurements updated.")

	def update_field_config(self, field_id: str, config: dict) -> None:
		"""Update irrigation configuration of the field"""
		if field_id in self.fields:	
			field = self.fields[field_id]

			# Update field's config values
			if 'target_humidity' in config:
				field.target_humidity = config['target_humidity']

			if 'min_humidity' in config:
				field.min_humidity = config['min_humidity']

			if 'max_watering_time' in config:
				field.max_watering_time = config['max_watering_time']
			
			logging.info(f"[{field_id}] Configuration updated: {config}")
		
		else:
			self.fields[field_id] = FieldIrrigation(field_id, config or {}, self.sensors_scheduler)
			
	def run_cycle(self, field_id: str) -> None:
		"""Run irrigation for a specific field"""
		if field_id in self.fields:
			self.fields[field_id].smart_irrigation()

	def run_all_cycles(self):
		"""Run irrigation for all fields"""
		if self.fields is None:
			logging.info('Empty list for irrigation system')

		user_ids = get_user_ids()
		for id in user_ids:
			# Send alert
			alert(
				user_id=id,
				message="Irrigation cycle started.",
				type="INFO"
			)

		for field in self.fields:
			self.run_cycle(field)

		for id in user_ids:
			# Send alert
			alert(
				user_id=id,
				message="Irrigation cycle succesfully run.",
				type="INFO"
			)
	
	def schedule_irrigation_cycles(self, interval: int):
		"""Schedule automatic irrigation cycles"""
		if not self.scheduler.get_job('irrigation_cycle'):
			self.scheduler.add_job(
				id='irrigation_cycle',
				func=self.run_all_cycles,
				trigger='interval',
				seconds=interval
			)

			# Initialize fields in case of a reset
			self.system_init()

			logging.info(f'Scheduled irrigation cycles every {interval} seconds')

	def pause_irrigation_system(self):
		"""Pause the periodic irrigation job"""
		job = self.scheduler.get_job('irrigation_cycle')

		if job:
			job.pause()
			logging.info('Paused irrigation system')

		else:
			logging.warning('Irrigation system job not found to pause')

	def resume_irrigation_system(self):
		"""Resume the periodic irrigation job"""
		job = self.scheduler.get_job('irrigation_cycle')

		if job:
			job.resume()
			logging.info('Resumed irrigation system')

		else:
			logging.warning('Irrigation system job not found to resume')

	def update_interval(self, new_interval: int) -> None:
		"""Update timer of irrigations"""
		job  = self.scheduler.get_job('irrigation_cycle')
		
		if job:
			self.scheduler.scheduler.reschedule_job(
				job_id='irrigation_cycle',
				trigger='interval',
				seconds=new_interval
			)
			logging.info(f'Irrigation timer updated to run every {new_interval} seconds')

		else:
			logging.warning('Irrigation update job not found to update interval')

