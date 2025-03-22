from src.classes.SensorType import *

class Sensor:
	def __init__(self, name: str, type: type, field_id: str):
		self.name = name
		self.type = type
		self.field_id = field_id

	def to_dict(self)  -> dict:
		return {
			"name": self.name,
			"type": self.type.to_dict(),
			"field_id": self.field_id
		}
	
	@staticmethod
	def from_dict(data: dict) -> "Sensor":
		sensor_type = SensorType(
			type=data["type"]["type"],
			measured_value=data["type"]["measured_value"],
			status=data["type"]["status"],
			port=data["type"]["port"]
		)
		return Sensor(name=data["name"], type=sensor_type, field_id=data.get("field_id"))
