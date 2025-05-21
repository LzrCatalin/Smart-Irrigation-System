import logging
from colorama import Fore, Style
from firebase_admin import credentials, db
from src.firebase.db_init import db_init
from src.classes.Sensor import Sensor
from src.classes.Type import Type
from src.classes.Status import Status
from src.classes.SensorDTO import SensorDTO

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
def get_sensors_ids() -> list[str]:
	logging.info("Fetching sensor IDs...")
	# Fetch data
	sensors_data = REF.get()

	if sensors_data is None:
		logging.warning("No sensors ids found.")
		return []

	# Populate ids array
	sensor_ids = list(sensors_data.keys())

	logging.info(f"Sensor IDs: {sensor_ids}")
	return sensor_ids

#
#	Retrieve all sensors data
#
def get_sensors_data() -> list[dict]:
	logging.info("Fetching sensors data...")

	# Fetch data
	sensors_data = REF.get()

	logging.info("Successfully retrieved sensors data")
	return sensors_data

#
# 	Retrieve sensor data by ID
#
def get_sensor_data_by_id(sensor_id: str) -> dict:
	logging.info(f"Fetching data for id: {sensor_id}")
	
	sensor_data = REF.child(sensor_id).get()

	# Check if data exists
	if sensor_data is None:
		return {"error": f"No data found for ID: {sensor_id}"}
	
	try:
		sensor = Sensor.from_dict(sensor_data)
		sensorDTO = SensorDTO(id=sensor_id, name=sensor.name, type=sensor.type, field_id=sensor.field_id)
		logging.info(f"Successfully fetched data for sensor ID: {sensor_id}")
		
		return sensorDTO.to_dict()

	except KeyError as e:
		logging.error(Fore.RED + 
				f"Error processing data for sensor ID {sensor_id}: {e}" + 
				Style.RESET_ALL)
		return None


#
#	Retrieve sensors data by Type
#
def get_sensors_data_by_type(sensors_type: type) -> list[dict]:
	logging.info(f"Fetching sensors data for type: {sensors_type}")

	# Fetch data
	sensors_data = REF.get()

	if sensors_data is None:
		logging.warning("No sensors found.")
		return []

	# Filter data
	filtered_sensors = {}
	
	for key, val in sensors_data.items():
		if val['type']['type'] == sensors_type:
			filtered_sensors[key] = val

	return filtered_sensors


#
#	Fetch sensor by name
#
def get_sensor_by_name(name: str) -> dict:
	logging.debug(f"Fetching sensor with name: {name}")

	# Fetch data
	sensor_data = REF.order_by_child('name').equal_to(name).get()

	# Verify data
	if sensor_data is None:
		return {"error": f"No data found for sensor name: {name}"}
	
	for firebase_id, data in sensor_data.items():
		return {
			'firebase_id': firebase_id,
			'sensor_data': data
		}


#
#	Check if port is in use
#
def is_port_in_use(port: int, sensor_type: type) -> bool:
	# Fetch sensors from db
	sensors_data = get_sensors_data_by_type(sensor_type)
	logging.debug(f"{sensors_data}")

	if sensors_data:
		for _, sensors_data in sensors_data.items():
			if sensors_data['type']['port'] == port:
				logging.warning(Fore.LIGHTYELLOW_EX +
					f"Port: {port} already in use for type: {sensor_type}" +
					Style.RESET_ALL)
				return True
	
	return False

#######################
#
#   CRUD Operations
#
#######################

#
#	Add 
#
def add_sensor(data: Sensor) -> dict:

	try:
		# Check port 
		if not is_port_in_use(data.type.port, data.type.type):
			
			# Push data into db
			sensor_ref = REF.push(data.to_dict())
			
			sensorDTO = SensorDTO(sensor_ref.key, data.name, data.type, data.field_id)

			logging.info(Fore.GREEN + 
				"Successfully added new sensor data." +
				Style.RESET_ALL)

			return sensorDTO.to_dict()
		
		else:
			return {"error": f"Port {data.type.port} already in use for type: {data.type.type}"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#
#	Update
#
def update_sensor_by_id(sensor_id: str, sensor: Sensor) -> dict:

	logging.debug(f"\t\t-> UPDATE SENSOR\n\t -> Details:\n\t{sensor_id}\n\t{sensor}")
	try:
		# Fetch old sensor data
		get_sensor_data_by_id(sensor_id)

		# if is_port_in_use(sensor.type.port, sensor.type.type):
		# 	if fetched_sensor['type']['port'] != sensor.type.port:
		# 		return {"error": f"Port: {sensor.type.port} already in use."}

		REF.child(sensor_id).set(sensor.to_dict())

		logging.info(Fore.GREEN + 
			   f"Successfully updated sensor data for ID: {sensor_id}" + 
			   Style.RESET_ALL)
		
		return sensor.to_dict()

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

#
#	Delete
#
def detele_sensor_by_id(sensor_id: str) -> None:
	try:
		# Verify ID in database
		fetched_sensor = get_sensor_data_by_id(sensor_id)
		
		# Delete sensor
		REF.child(sensor_id).delete()

		logging.info(Fore.GREEN + 
					f"Successfully delete data for sensor id: {sensor_id}" +
					Style.RESET_ALL)
		
		return fetched_sensor
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Fetch sensors by status
#
def fetch_sensors_by_status(sensors_status: str) -> list[dict]:
	try:
		# Convert status to uppercase to ensure consistency
		status_str = sensors_status.upper()

		# Fetch sensors from db
		sensors = get_sensors_data()

		# Retrieve sensors of expected status
		filtered_sensors = {}
		for sensor_id, sensor_data in sensors.items():
			logging.debug(f"ID: {sensor_id} -> Data: {sensor_data}")
			if sensor_data.get("type", {}).get("status", "") == status_str:
				filtered_sensors[sensor_id] = sensor_data

		if not filtered_sensors:
			return {"error": f"No sensors with status: {status_str}"}
		
		return filtered_sensors
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	

#
#	Set AVAILABLE status using name
#
def set_available_status(sensor_name: str) -> None:
	try:
		# Fetch sensor by name
		sensor_result = get_sensor_by_name(sensor_name)

		# Fetch sensor data and firebase ID based on dict
		sensor = sensor_result['sensor_data']
		sensor_id = sensor_result['firebase_id']

		# Update status and firebase
		sensor["type"]["status"] = Status.AVAILABLE.name
		REF.child(sensor_id).set(sensor)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	

#
#	Set NOT_AVAILABLE status using ID
#
def set_not_available_status(id: str) -> None:
	try:
		# Fetch sensor by ID
		sensor = get_sensor_data_by_id(id)

		# Update status and firebase
		sensor["type"]["status"] = Status.NOT_AVAILABLE.name
		REF.child(id).set(sensor)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#
#	Set field id attribute for sensor
#
def set_sensor_field_id(id: str, field_id: str) -> None:
	try:
		# Fetch sensor by id
		sensor = get_sensor_data_by_id(id)

		# Update field id
		sensor["field_id"] = field_id
		REF.child(id).set(sensor)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#
#	Unset field id attribute for sensor
# 
def unset_sensor_field_id(sensor_name: str) -> None:
	try:
		# Fetch sensor by name
		sensor_result = get_sensor_by_name(sensor_name)

		# Fetch sensor data and firebase ID based on dict
		sensor = sensor_result['sensor_data']
		sensor_id = sensor_result['firebase_id']

		# Update status and firebase
		sensor["field_id"] = "None"
		REF.child(sensor_id).set(sensor)

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}