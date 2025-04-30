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
			print(f'Adding id: {field_id}')
			self.fields[field_id] = FieldIrrigation(field_id, config or {}, self.sensors_scheduler)

	def update_field_measurements(self, field_id: str, humidity: float, temperature: float, port: int) -> None:
		"""Update measurements of the field"""
		if field_id in self.fields:
			print(f'Updating field id: {field_id}')
			self.fields[field_id].current_humidity = humidity
			self.fields[field_id].current_temperature = temperature
			self.fields[field_id].current_port = port

	def run_cycle(self, field_id: str) -> None:
		"""Run irrigation for a specific field"""
		if field_id in self.fields:
			self.fields[field_id].smart_irrigation()

	def run_all_cycles(self):
		"""Run irrigation for all fields"""
		if self.fields is None:
			print('Empty list.')

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