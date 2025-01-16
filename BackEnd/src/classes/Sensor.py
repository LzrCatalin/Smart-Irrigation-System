from src.classes.SensorType import *

class Sensor:
	def __init__(self, name: str, type: type):
		self.name = name
		self.type = type

	def to_dict(self)  -> dict:
		return {
			"name": self.name,
			"type": self.type.to_dict()
		}
	
	@staticmethod
	def from_dict(data: dict) -> "Sensor":
		sensor_type = SensorType(
			type=data["type"]["type"],
			measured_value=data["type"]["measured_value"],
			status=data["type"]["status"],
			port=data["type"]["port"]
		)
		return Sensor(name=data["name"], type=sensor_type)
