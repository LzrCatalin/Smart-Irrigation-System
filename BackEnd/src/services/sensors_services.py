import logging
from colorama import Fore, Style
from firebase_admin import credentials, db
from src.firebase.db_init import db_init
from src.classes.Sensor import Sensor
from src.classes.Type import *
from src.classes.Status import *

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
		logging.info(Fore.WHITE +
			"No available sensors ... " +
			Style.RESET_ALL)
		return None

	logging.info("Successfully retrieved sensors data")
	return sensors_data

#
# 	Retrieve sensor data by ID
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

#
#	Retrieve sensors data by Type
#
def get_sensors_data_by_type(sensors_type):
	logging.info(f"Fetching sensors data for type: {sensors_type}")

	# Fetch data
	sensors_data = REF.get()

	# Filter data
	filtered_sensors = {}
	
	for sensor_data in sensors_data:
		if sensor_data is None:
			continue
		
		# Retrieve type for comparing	
		type = sensor_data['type']['type']

		if type == sensors_type:
			id = sensor_data['id']
			# Append sensor into map
			filtered_sensors[id] = sensor_data

	return filtered_sensors

#
#	Verify duplicate ports
#
def is_port_in_use(port, sensor_type):
	# Fetch sensors from db
	sensors_data = get_sensors_data_by_type(sensor_type)

	if sensors_data:
		# Iterate sensors
		for id, sensor_data in sensors_data.items():
			print(f"ID: {id}")
			print(f"SENSOR_DATA: {sensor_data}")
			print(f"Port: {sensor_data['type']['port']}")
			# Search for port in each sensors ports
			if sensor_data['type']['port'] == port:
				print("Port already exists.")
				return True
	
	print("Port not found.")
	return False

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
		type = data['type']['type']
		measured_value = data['type']['measured_value']
		status = data['type']['status']
		port = data['type']['port']

		# Convert data to enum
		type = Type[type.upper()]
		status = Status[status.upper()]

		# # Verify duplicate port based on sensor's type
		if is_port_in_use(port, type.name):
			logging.info("\t\tPort condition.")
			logging.warning(Fore.LIGHTYELLOW_EX +
				   f"Port: {port} already in use for type: {type}"
				   + Style.RESET_ALL)
			return
		
		# Create object of type sensor with fetched data
		object = {
			'id': id,
			'name': name,
			# Create the sensor type 
			'type': {
				'type': type.name,
				'measured_value': measured_value,
				'status': status.name,
				'port': port
			}
		}

		# Push data into db
		REF.child(f"{id}").set(object)
		
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
		type = data['type']['type']
		measured_value = data['type']['measured_value']
		status = data['type']['status']
		port = data['type']['port']

		# Convert data to enum
		type = Type[type.upper()]
		status = Status[status.upper()]

		# Create object of type sensor with fetched data
		object = {
			'id': id,
			'name': name,
			# Create the sensor type 
			'type': {
				'type': type.name,
				'measured_value': measured_value,
				'status': status.name,
				'port': port
			}
		}
		
		# Push new data into database
		REF.child(f"{sensor_id}").set(object)

		logging.info(Fore.GREEN + 
			f"Successfully updated sensor data for id: {sensor_id}" 
			+ Style.RESET_ALL)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

#
#	Delete
#
def detele_sensor_by_id(sensor_id):
	# Delete sensor
	REF.child(f"{sensor_id}").delete()

	logging.info(Fore.GREEN + 
	   f"Successfully delete data for sensor id: {sensor_id}" +
	   Style.RESET_ALL)
