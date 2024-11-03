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
REF = db.reference(f'{DB_REF}')

#
#	Retrieve all sensors ids
#
def get_sensors_ids():
    logging.info("Fetching sensor IDs...")
    # Fetch data
    sensors_data = REF.get()
    print(sensors_data)

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

    # Add data with custom ID
    REF.child(f"{id_sensor}").set({
        'id': id_sensor,
        'sensor_name' : sensor.name,
        'temperature': sensor.temperature,
        'humidity': sensor.humidity,
        'port': sensor.port,
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
    existing_sensor.id = update_data.id 
    existing_sensor.name = update_data.name 
    existing_sensor.temperature = update_data.temperature 
    existing_sensor.humidity = update_data.humidity
    existing_sensor.port = update_data.port
    
    # Update sensor
    REF.child(f"{sensor_id}").set({
        'id': existing_sensor.id,
        'sensor_name': existing_sensor.name,
        'temperature': existing_sensor.temperature,
        'humidity': existing_sensor.humidity,
        'port': existing_sensor.port,
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

    # Delete if id found
    REF.child(f"{sensor_id}").delete()
    logging.info(Fore.GREEN + 
       f"Successfully delete data for sensor id: {sensor_id}" +
       Style.RESET_ALL)
