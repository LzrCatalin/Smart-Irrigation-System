import logging
from colorama import Fore, Style
from firebase_admin import credentials, db
from src.firebase.custom_id import id_incrementation
from src.firebase.db_init import db_init
from src.classes.Sensor import Sensor

# Database init
db_init()

#######################
#
#   Database path for sensors
#
#######################
DB_REF = 'irrigation-system/sensor_data'

#
#	Retrieve all sensors ids
#
def get_sensors_ids():
	logging.info("Fetching sensor IDs...")
	ref = db.reference(f'{DB_REF}')
	sensors_data = ref.get()
	
	sensor_ids = []
	# Iterate through the list of sensors from db
	for index, sensor in enumerate(sensors_data):
		# Hardcoded each sensor id
		if sensor is not None:
			sensor_id = str(index)
			sensor_ids.append(sensor_id)
	
	logging.info(f"Sensor IDs: {sensor_ids}")
	return sensor_ids

#
#	Retrieve all sensors data
#
def get_sensors_data():
	logging.info("Fetching sensors data...")
	ref = db.reference(f'{DB_REF}')

	sensors_data = ref.get()

	if sensors_data is None:
		logging.warning(Fore.YELLOW +
			"No available sensors ... " +
			Style.RESET_ALL)

	logging.info("Successfully retrieved sensors data")
	return sensors_data

#
# Retrieve sensor data by ID
#
def get_sensor_data(sensor_id):
	logging.info(f"Fetching data for id: {sensor_id}")
	
	# Path to fetch wanted data
	ref = db.reference(f'{DB_REF}/{sensor_id}')
	sensor_data = ref.get()

	# Check if data exists
	if sensor_data is None:
		logging.warning(f"No data found for sensor with id: {sensor_id}")
		return None
	
	logging.info(f"Successfully fetched data for sensor id: {sensor_id}")
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
	logging.info(f"Add Process: Sensor id: {id_sensor}")

	# Fetch path
	ref = db.reference(f'{DB_REF}')

	# Add data with custom ID
	ref.child(f"{id_sensor}").set({
		'sensor_name' : sensor.name,
		'temperature': sensor.temperature,
		'humidity': sensor.humidity,
		'timestamp':  {".sv": "timestamp"}
	})

	logging.info(Fore.GREEN + 
	   "Successfully added new sensor data." +
	   Style.RESET_ALL)

#
#	Update
#
def update_sensor_by_id(sensor_id, update_data):
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

	logging.info(Fore.GREEN + 
	   f"Successfully updated sensor data for id: {sensor_id}" 
	   + Style.RESET_ALL)

#
#	Delete
#
def detele_sensor_by_id(sensor_id):
	logging.info(f"Delete sensor id: {sensor_id}")
	# Fetch sensor with id
	get_sensor_data(sensor_id)

	# Fetch path
	ref = db.reference(f'{DB_REF}')

	# Delete if id found
	ref.child(f"{sensor_id}").delete()
	logging.info(Fore.GREEN + 
	   f"Successfully delete data for sensor id: {sensor_id}" +
	   Style.RESET_ALL)