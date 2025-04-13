import time

from typing import Dict
# from src.classes.FieldIrrigation import FieldIrrigation
from FieldIrrigation import FieldIrrigation

class FieldIrrigationSystem:
	"""Store fields that needs to be managed"""
	def __init__(self):
		self.fields: Dict[str, FieldIrrigation] = {}
		
	def add_field(self, field_id: str, config: dict = None) -> None:
		"""Add a new field to be managed"""
		if field_id not in self.fields:
			self.fields[field_id] = FieldIrrigation(field_id, config or {})

	def update_field_measurements(self, field_id: str, humidity: float, temperature: float) -> None:
		"""Update measurements of the field"""
		if field_id in self.fields:
			self.fields[field_id].current_humidity = humidity
			self.fields[field_id].current_temperature = temperature

	def run_cycle(self, field_id: str) -> None:
		"""Run irrigation for a specific field"""
		if field_id in self.fields:
			self.fields[field_id].smart_irrigation()

	def run_all_cycles(self):
		"""Run irrigation for all fields"""
		for field in self.fields:
			self.run_cycle(field)


if __name__ == "__main__":
	
	irrigation_system = FieldIrrigationSystem()

	config = {
		'target_humidity': 90,
		'min_humidity': 30,
		'max_watering_time': 500
	}
	field_id = 'ID_1'

	irrigation_system.add_field(field_id, config)
	irrigation_system.update_field_measurements(field_id, 53.30, 23.2)

	irrigation_system.run_cycle(field_id)


	"""
		TODO: 
			- Create an init function, that store all the fields
		available in db into the system fields in case of reset
			- At each field add, store it into the system fields,
		but, make sure the fields has both humidity and temperature
		sensors
			- On update schedule too , make sure the values updates
	"""