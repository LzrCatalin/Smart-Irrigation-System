from firebase_admin import credentials, db
from firebase.custom_id import id_incrementation
from firebase.db_init import db_init
from classes.Sensor import Sensor

# Database init
db_init()

#######################
#
#   Database path for sensors
#
#######################
DB_REF = 'irrigation-system/sensor_data'

#
#	Retrieve all sensors data
#
def get_sensors_data():
	# TODO : Work on return statement
	print("Retrieving all sensors ... ")
	ref = db.reference(f'{DB_REF}')

	sensors_data = ref.get()

	if sensors_data is None:
		print("No available sensors ... ")

	print("Successfully retrieved sensors data")
	return sensors_data

#
# Retrieve sensor data by ID
#
def get_sensor_data(sensor_id):

	# TODO : Work on logical part
	print(f"Retriving data for id: {sensor_id}")
	
	# Path to fetch wanted data
	ref = db.reference(f'{DB_REF}/{sensor_id}')
	sensor_data = ref.get()

	# Check if data exists
	if sensor_data is None:
		print(f"No data found for sensor with id: {sensor_id}")
		return 404
	
	print(f"Successfully retrieved data for sensor id: {sensor_id}")
	return sensor_data

#######################
#
#   CRUD Operations
#
#######################

#
#	Add 
#
def add_sensor(sensor):
	id_sensor = id_incrementation('sensor')
	print(f"Add sensor with id: {id_sensor}")

	# Fetch path
	ref = db.reference(f'{DB_REF}')

	# Add data with custom ID
	ref.child(f"{id_sensor}").set({
		'sensor_name' : sensor.name,
		'temperature': sensor.temperature,
		'humidity': sensor.humidity,
		'timestamp':  {".sv": "timestamp"}
	})

	print("Successfully added sensor data.")

#
#	Update
#
def update_sensor_by_id(sensor_id, update_data):
	print("Inside update sensor function ...")
	# Fetch sensor with id
	updated_sensor = get_sensor_data(sensor_id)

	# Convert data to Sensor object
	existing_sensor = Sensor.from_dict(updated_sensor)

	# Update attribut if there is a new value
	existing_sensor.name = update_data.name if update_data.name else existing_sensor.name
	existing_sensor.temperature = update_data.temperature if update_data.temperature else existing_sensor.temperature
	existing_sensor.humidity = update_data.humidity if update_data.humidity else existing_sensor.humidity
	
	# Fetch path
	ref = db.reference(f'{DB_REF}')

	# Update sensor	
	ref.child(f"{sensor_id}").set({
		'sensor_name': existing_sensor.name,
		'temperatur': existing_sensor.temperature,
		'humidity': existing_sensor.humidity,
		'timestamp':  {".sv": "timestamp"}
	})

	print(f"Successfully updated sensor data for id: {sensor_id}")

#
#	Delete
#
def detele_sensor_by_id(sensor_id):
	print(f"Deleting sensor id: {sensor_id} ...")

	# Fetch sensor with id
	get_sensor_data(sensor_id)

	# Fetch path
	ref = db.reference(f'{DB_REF}')

	# Delete if id found
	ref.child(f"{sensor_id}").delete()
	print(f"Successfully delete data for sensor id: {sensor_id}")
