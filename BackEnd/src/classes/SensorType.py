class SensorType:
	def __init__(self, type, measured_value, status, port):
		self.type = type
		self.measured_value = measured_value
		self.status = status
		self.port = port

	def to_dict(self) -> dict:
		return {
			"type": self.type,
			"measured_value": self.measured_value,
			"status": self.status,
			"port": self.port
		}
