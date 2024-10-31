class Sensor:
	def __init__(self, id, name, humidity, temperature, port):
		self.id = id
		self.name = name
		self.temperature = temperature
		self.humidity = humidity
		self.port = port

	def __str__(self):
		return f"----\nSensor name: {self.name}\nTemperature: {self.temperature:.1f}C\nHumidity: {self.humidity:.2f}%\nSensor port: {self.port}"

	##########################
	#
	#   Change database JSON to class object
	#
	###########################
	@classmethod
	def from_dict(obj, data):
		return obj(
			id = data.get('id'),
			name = data.get('sensor_name'),
			temperature = data.get('temperature'),
			humidity = data.get('humidity'),
			port = data.get('port')
		)


