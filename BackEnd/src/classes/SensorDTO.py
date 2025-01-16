from src.classes.SensorType import *

class SensorDTO:
	def __init__(self, id: str, name: str, type:type):
		self.id = id
		self.name = name
		self.type = type

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
			"type": self.type.to_dict()
		}
	
	@staticmethod
	def from_dict(data: dict) -> "SensorDTO":
		return SensorDTO(
			id = data.get("id"),
			name = data.get("name"),
			type = data.get("type")
		)