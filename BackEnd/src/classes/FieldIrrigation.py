import time
import logging

from src.services.fields_service import get_field_user
from src.services.fields_service import get_location_by_field_id
from src.util.utils import alert
from src.util.mail_sender import send_email
from src.actuators.water_pump import pump_start, pump_stop
from src.sensors.humidity_sensor import sensor_setup, moisture_percentage
from src.services.history_service import add_irrigation

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

	def is_critical_humidity(self) -> None:
		"""Alert user when the current humidity is less than configured minimal"""
		# Fetch field's user
		user_id = get_field_user(self.field_id)
		# Fetch field's location
		field_location = get_location_by_field_id(self.field_id)

		# Verify critical level
		if (self.current_humidity < self.min_humidity):
			
			# Send alert
			alert(
				user_id=user_id,
				message=f"Field on [{field_location[8:]}] below minimum humidity.",
				type="WARNING"
			)

			# Send emal: TODO
			# send_email(

			# )
			

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

				# Add history
				add_irrigation(self.field_id)

				# Resume sensors updates
				if self.sensors_scheduler:
					self.sensors_scheduler.resume_sensor_updates()

		else:
			logging.info(f'[{self.field_id}] Humidity OK ({self.current_humidity})')	


