import time
import logging

from src.actuators.water_pump import pump_start, pump_stop
from src.sensors.humidity_sensor import sensor_setup, moisture_percentage

class FieldIrrigation:
	def __init__(self, field_id: str, config: dict, sensors_scheduler: None):
		self.field_id = field_id
		self.current_humidity = 0
		self.current_temperature = 0
		self.current_port = None
		self.pump_running = False
		self.last_irrigation = 0

		self.sensors_scheduler = sensors_scheduler

		# Configurable parameters (with default values if no config)
		self.target_humidity = config.get('target_humidity', 60)
		self.min_humidity = config.get('min_humidity', 10)
		self.max_watering_time = config.get('max_watering_time', 300)

	def control_pump(self, state: bool):
		"""Control the water for the field"""
		self.pump_running = state

		if self.pump_running:
			pump_start()
			logging.debug(f'[{self.field_id}] Pump \'ON\'')
		
		else:
			pump_stop()
			logging.debug(f'[{self.field_id}] Pump \'OFF\'')
		
	def smart_irrigation(self) -> None:
		"""Irrigation system implementation"""
		current_time = time.time()

		# Check if watering is needed
		if self.current_humidity < self.min_humidity:
			logging.info(f'[{self.field_id}] Low humidity: ({self.current_humidity}%). Starting irrigation.')

			# Pause sensors updates
			if self.sensors_scheduler:
				self.sensors_scheduler.pause_sensor_updates()

			# Turn ON the water pump
			self.control_pump(True)
			start_time = current_time

			try:
				print(f'Pump state: {self.pump_running}')
				while self.pump_running:
					elapsed = time.time() - start_time

					# Fetch data about humidity and check the improvements
					new_humidity = moisture_percentage(sensor_setup(self.current_port))
					print(f'Measure humidity in the process: {new_humidity}')

					# Stop conditions
					if new_humidity >= self.target_humidity:
						logging.info(f'[{self.field_id}] Target reached ({new_humidity}%)')
						break
				
					elif elapsed >= self.max_watering_time:
						logging.info(f'[{self.field_id}] Max watering time reached')
						break
					
					print('Remaking the process')
					time.sleep(2)
			
			finally:
				self.control_pump(False)
				self.last_irrigation = time.time()
				logging.info(f'[{self.field_id}] Irrigation complete')

				# Resume sensors updates
				if self.sensors_scheduler:
					self.sensors_scheduler.resume_sensor_updates()

		else:
			logging.info(f'[{self.field_id}] Humidity OK ({self.current_humidity})')	


