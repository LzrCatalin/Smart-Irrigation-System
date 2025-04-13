import logging

# from src.actuators.water_pump import pump_start, pump_stop

class FieldIrrigation:
	def __init__(self, field_id: str, config: dict):
		self.field_id = field_id
		self.current_humidity = 0
		self.current_temperature = 0
		self.last_irrigation = 0

		# Configurable parameters (with default values if no config)
		self.target_humidity = config.get('target_humidity', 60)
		self.min_humidity = config.get('min_humidity', 10)
		self.max_watering_time = config.get('max_watering_time', 300)

	# def control_pump(self, state: bool):
	# 	"""Control the water for the field"""
	# 	if state:
	# 		pump_start()
	# 		logging.debug(f'[{self.field_id}] Pump \'ON\'')
		
	# 	else:
	# 		pump_stop()
	# 		logging.debug(f'[{self.field_id}] Pump \'OFF\'')

	def smart_irrigation(self) -> None:
		print(f'Field_ID: {self.field_id}')
		print(f' -> Field humidity: {self.current_humidity}')
		print(f' -> Field temperature: {self.current_temperature}')
		print(f' -> Target humidity: {self.target_humidity}')
		print(f' -> Min humidity: {self.min_humidity}')
		print(f' -> Max watering time: {self.max_watering_time}')
		print('Incoming')

