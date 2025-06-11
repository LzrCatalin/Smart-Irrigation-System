import time
import logging

from src.classes.Field import Field
from src.util.utils import alert
from src.util.mail_sender import send_email, generate_critical_humidity_alert

from src.api.weatherAPI import retrieve_weather_data
from src.actuators.water_pump import pump_start, pump_stop

from src.services.users_service import get_user_by_id
from src.services.history_service import add_irrigation
from src.services.fields_service import get_location_by_field_id
from src.services.fields_service import get_field_user, get_field_by_id, update_field_measurements_by_id

from src.sensors.humidity_sensor import sensor_setup, moisture_percentage

class FieldIrrigation:
	def __init__(self, field_id: str, config: dict, sensors_scheduler: None):
		self.field_id = field_id
		self.current_humidity = 0
		self.current_temperature = 0
		self.current_port = None
		self.pump_running = False

		self.sensors_scheduler = sensors_scheduler

		# Configurable parameters (with default values if no config)
		self.target_humidity = config.get('target_humidity', 60)
		self.min_humidity = config.get('min_humidity', 10)
		self.max_watering_time = config.get('max_watering_time', 300)

	def patch_field_after_irrigation(self, humidity_value: float) -> None:
		"""Update humidity sensor's measured value after irrigation"""
		field_data = get_field_by_id(self.field_id)

		# Verification
		if not field_data:
			logging.warning(f"[{self.field_id}] Field data not found for update.")
			return

		# Search for humidity sensor
		for sensor in field_data.get('sensors', []):
			if sensor['type']['type'] == "HUMIDITY":
				sensor['type']['measured_value'] = humidity_value
				break
		else:
			logging.warning(f"[{self.field_id}] No HUMIDITY sensor found to patch.")
			return

		# Convert to Field object
		updated_field = Field.from_dict(field_data)

		# Update in database
		result = update_field_measurements_by_id(self.field_id, updated_field)

		if "error" in result:
			logging.error(f"[{self.field_id}] Failed to patch humidity: {result['error']}")
		else:
			logging.info(f"[{self.field_id}] Updated sensor humidity to: {humidity_value:.2f}%")


	def is_critical_humidity(self) -> None:
		"""Alert user when the current humidity is less than configured minimal"""
		# Fetch field's user
		user_id = get_field_user(self.field_id)
		field_data = get_field_by_id(self.field_id)

		# Fetch field's location
		field_location = get_location_by_field_id(self.field_id)

		# Verify critical level
		if (self.current_humidity < self.min_humidity):
			
			# Send alert
			alert(
				user_id=user_id,
				message=f"Field from [{field_location[8:]}] below minimum humidity.",
				type="WARNING"
			)

			# Send emal
			send_email("Critical Humidity Alert",
				generate_critical_humidity_alert(
					get_user_by_id(user_id)['email'],
					field_location[8:],
					field_data['crop_name'],
					self.current_humidity, 
					self.min_humidity
				),
				get_user_by_id(user_id)['email']
			)	

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
		"""Irrigation system implementation enhanced with weather data"""

		current_time = time.time()

		# Get field location and extract city and user
		location_str = get_location_by_field_id(self.field_id)
		city_name = location_str.split(',')[0].strip()
		user_id = get_field_user(self.field_id)

		# Retrieve weather data
		weather = retrieve_weather_data(city_name)

		if not weather:
			logging.warning(f"[{self.field_id}] Failed to retrieve weather data. Proceeding with default logic.")
		
		else:
			# Check rain condition
			if "rain" in weather['condition'].lower() or weather['precip_mm'] > 0.1:
				logging.info(f"[{self.field_id}] Rain expected or ongoing ({weather['condition']}, {weather['precip_mm']}mm). Skipping irrigation.")
				return

			# Adjust watering time based on temp & humidity
			if weather['temp'] > 30:
				self.max_watering_time *= 1.2
				logging.info(f"[{self.field_id}] High temperature ({weather['temp']}°C). Increasing watering time.")

			elif weather['humidity'] > 70:
				self.max_watering_time *= 0.85
				logging.info(f"[{self.field_id}] High air humidity ({weather['humidity']}%). Reducing watering time.")

		# Check if irrigation is necessary
		if self.current_humidity < self.target_humidity:
			logging.info(f'[{self.field_id}] Low soil humidity: ({self.current_humidity}%). Starting irrigation.')

			# Start irrigation
			self.control_pump(True)
			start_time = current_time

			try:
				while self.pump_running:
					elapsed = time.time() - start_time
					new_humidity = moisture_percentage(sensor_setup(self.current_port))
					logging.debug(f'[{self.field_id}] Measuring humidity: {new_humidity}%')

					# Alert the user in case the sensor 
					if new_humidity < 0 or new_humidity > 100:
						alert(user_id, f"Faulty Humidity Sensor on field [{location_str[8:]}].", type="ERROR")
						break

					if new_humidity >= self.target_humidity:
						logging.info(f'[{self.field_id}] Target soil humidity reached: {new_humidity}%')
						break

					elif elapsed >= self.max_watering_time:
						logging.info(f'[{self.field_id}] Maximum watering time reached.')
						break

					time.sleep(2)

			finally:
				self.control_pump(False)
				self.last_irrigation = time.time()
				logging.info(f'[{self.field_id}] Irrigation complete.')

				# Add to history
				add_irrigation(self.field_id)

		else:
			logging.info(f'[{self.field_id}] Soil humidity OK: {self.current_humidity}%')	


