import firebase_admin
from firebase_admin import credentials, db
from firebase.custom_id import id_incrementation
from firebase.db_init import db_init

# Database init
db_init()

#######################
#
#   Fetch data for sensors
#
#######################
ref = db.reference('irrigation-system/sensor_data')

# Fetch sensor data by ID
def get_sensor_data(sensor_id):
	print(f"Retriving data for id: {sensor_id}")
	
	ref = db.reference(f'irrigation-system/sensor_data/{sensor_id}')
	sensor_data = ref.get()

	if sensor_data:
		print(f"Sensor data for {sensor_id}: {sensor_data}")

	else:
		print(f"No data found for sensor with id: {sensor_id}")

#######################
#
#   CRUD Operations
#
#######################
def add_sensor(sensor):
	id_sensor = id_incrementation('sensor')
	print(f"Add sensor with id: {id_sensor}")

	# Add data with custom ID
	ref.child(f"{id_sensor}").set({
		'sensor_name' : sensor.name,
		'temperature': sensor.temperature,
		'humidity': sensor.humidity,
		'timestamp':  {".sv": "timestamp"}
	})

	print("Successfully added sensor data.")

def update_sensor_by_id(sensor_id):
	# TODO: Implementation
	return 0

def detele_sensor_by_id(sensor_id):
	# TODO: implementation
	return 0