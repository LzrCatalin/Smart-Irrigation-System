from src.classes.Sensor import *

class Field:

	def __init__(self, latitude: float, longitude: float, length: float, width: float, slope: float, 
				soil_type: str, crop_name: 
				str, user: str, sensors: list[Sensor] = None):
		
		self.latitude = latitude
		self.longitude = longitude
		self.length = length
		self.width = width
		self.slope = slope
		self.soil_type = soil_type
		self.crop_name = crop_name
		self.user = user
		self.sensors = sensors or []

	def to_dict(self) -> dict:
		return {
			"latitude": self.latitude,
			"longitude": self.longitude,
			"length": self.length,
			"width": self.width,
			"slope": self.slope,
			"soil_type": self.soil_type,
			"crop_name": self.crop_name,
			"user": self.user,
			"sensors": [sensor.to_dict() for sensor in self.sensors],
		}
	
	@staticmethod
	def from_dict(data: dict) -> "Field":
		field =  Field(
			latitude = data["latitude"],
			longitude = data["longitude"],
			length = data["length"],
			width = data["width"],
			slope = data["slope"],
			soil_type = data["soil_type"],
			crop_name = data["crop_name"],
			user = data["user"],
			sensors = [Sensor.from_dict(sensor) for sensor in data.get("sensors", [])],
		)

		return field
