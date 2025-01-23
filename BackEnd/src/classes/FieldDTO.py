from src.classes.Sensor import *

class FieldDTO:

	def __init__(self, id: str, 
				latitude: float, longitude: float, length: float, width: float, slope: float, 
				soil_type: str, crop_name: str, 
				user: str, sensors: list[dict]):
		
		self.id = id
		self.latitude = latitude
		self.longitude = longitude
		self.length = length
		self.width = width
		self.slope = slope
		self.soil_type = soil_type
		self.crop_name = crop_name
		self.user = user
		self.sensors = sensors

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"latitude": self.latitude,
			"longitude": self.longitude,
			"length": self.length,
			"width": self.width,
			"slope": self.slope,
			"soil_type": self.soil_type,
			"crop_name": self.crop_name,
			"user": self.user,
			"sensors": [sensor for sensor in self.sensors],
		}
	
	@staticmethod
	def from_dict(data: dict) -> "FieldDTO":
		fieldDTO = FieldDTO(
			id = data["id"],
			longitude = data["longitude"],
			length = data["length"],
			width = data["width"],
			slope = data["slope"],
			soil_type = data["soil_type"],
			crop_name = data["crop_name"],
			user = data["user"],
			sensors = data.get("sensors", []),
		)
		return fieldDTO
	
	
