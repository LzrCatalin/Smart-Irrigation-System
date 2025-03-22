from src.classes.SensorType import *

class SensorDTO:
	def __init__(self, id: str, name: str, type:type, field_id: str):
		self.id = id
		self.name = name
		self.type = type
		self.field_id = field_id

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
			"type": self.type.to_dict(),
			"field_id": self.field_id
		}
	
	@staticmethod
	def from_dict(data: dict) -> "SensorDTO":
		return SensorDTO(
			id = data.get("id"),
			name = data.get("name"),
			type = data.get("type"),
			field_id = data.get("field_id")
		)