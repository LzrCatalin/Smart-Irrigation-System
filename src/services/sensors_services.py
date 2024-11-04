import logging
from colorama import Fore, Style
from firebase_admin import credentials, db
from src.firebase.custom_id import id_incrementation
from src.firebase.db_init import db_init
from src.classes.Sensor import Sensor
from src.classes.Type import *

# Database init
db_init()

#######################
#
#   Database path for sensors
#
#######################
DB_REF = 'irrigation-system/sensor_data'
REF = db.reference(f'{DB_REF}')

#
#	Retrieve all sensors ids
#
def get_sensors_ids():
	logging.info("Fetching sensor IDs...")
	# Fetch data
	sensors_data = REF.get()

	if sensors_data is None:
		logging.warning("No sensors ids found.")
		return []

	# Populate ids array
	sensor_ids = []
	for sensor in sensors_data:
		if sensor is not None:
			sensor_ids.append(sensor['id'])

	logging.info(f"Sensor IDs: {sensor_ids}")
	return sensor_ids

#
#	Retrieve all sensors data
#
def get_sensors_data():
	logging.info("Fetching sensors data...")

	# Fetch data
	sensors_data = REF.get()

	if sensors_data is None:
		logging.warning(Fore.YELLOW +
			"No available sensors ... " +
			Style.RESET_ALL)
		return None

	logging.info("Successfully retrieved sensors data")
	return sensors_data

#
# Retrieve sensor data by ID
#
def get_sensor_data_by_id(sensor_id):
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
def add_sensor(data):
	try:
		# Fetch sensor data from JSON
		id = data['id']
		name = data['name']
		type_data = data['type']['type']
		measured_value = data['type']['measured_value']
		ports = data['type']['ports']

		# Convert type to enum value
		type = Type[type_data.upper()]

		# Create object of type sensor with fetched data
		object = {
			'id': id,
			'name': name,
			# Create the sensor type 
			'type': {
				'type': type,
				'measured_value': measured_value,
				'ports': ports
			}
		}

		REF.child(id).set(object)
		
		logging.info(Fore.GREEN + 
			"Successfully added new sensor data." +
			Style.RESET_ALL)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#
#	Update
#
def update_sensor_by_id(sensor_id, data):
	try: 
		# Fetch sensor data from JSON
		id = data['id']
		name = data['name']
		type_data = data['type']['type']
		measured_value = data['type']['measured_value']
		ports = data['type']['ports']

		# Convert type to enum value
		type = Type[type_data.upper()]

		# Create object of type sensor with fetched data
		object = {
			'id': id,
			'name': name,
			# Create the sensor type 
			'type': {
				'type': type,
				'measured_value': measured_value,
				'ports': ports
			}
		}
		
		# Push new data into database
		REF.child(sensor_id, object)

		logging.info(Fore.GREEN + 
			f"Successfully updated sensor data for id: {sensor_id}" 
			+ Style.RESET_ALL)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

#
#	Delete
#
def detele_sensor_by_id(sensor_id):
	logging.info(f"Delete sensor id: {sensor_id}")

	# Delete sensor
	REF.child(sensor_id).delete()

	logging.info(Fore.GREEN + 
	   f"Successfully delete data for sensor id: {sensor_id}" +
	   Style.RESET_ALL)
