import time
import logging

from typing import Dict
from flask_apscheduler import APScheduler
from src.classes.FieldIrrigation import FieldIrrigation

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
		
	def add_field(self, field_id: str, config: dict = None) -> None:
		"""Add a new field to be managed"""
		if field_id not in self.fields:
			self.fields[field_id] = FieldIrrigation(field_id, config or {}, self.sensors_scheduler)

	def update_field_measurements(self, field_id: str, humidity: float, temperature: float, port: int) -> None:
		"""Update measurements of the field"""
		if field_id in self.fields:
			self.fields[field_id].current_humidity = humidity
			self.fields[field_id].current_temperature = temperature
			self.fields[field_id].current_port = port

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

		for field in self.fields:
			self.run_cycle(field)
	
	def schedule_irrigation_cycles(self, interval: int):
		"""Schedule automatic irrigation cycles"""
		if not self.scheduler.get_job('irrigation_cycle'):
			self.scheduler.add_job(
				id='irrigation_cycle',
				func=self.run_all_cycles,
				trigger='interval',
				seconds=interval
			)
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

