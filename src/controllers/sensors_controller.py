from flask import Flask, jsonify, request, Blueprint
from http import HTTPStatus

####################
#
#   Add the path to the project
#
####################
import sys
sys.path.append("src")

from src.services import sensors_services
from src.classes.Sensor import *
from src.sensors.humidity_sensor import *
from src.sensors.testFunctions import *
from src.firebase.custom_id import id_incrementation

SENSORS_URL = '/api/sensors'

#
#   Setup Blueprint
#
sensors_bp = Blueprint('sensors', __name__, url_prefix= SENSORS_URL)

#
#   Get sensors
#
@sensors_bp.route('', methods = ['GET'])
def get_sensors():
	# Retrieve sensors data
	sensors_data = sensors_services.get_sensors_data()
	
	# Verify if data exists
	if sensors_data is None:
		return jsonify({"status:": "error",
						"message": "No sensors available"}), HTTPStatus.NOT_FOUND
	
	return jsonify(sensors_data), HTTPStatus.OK
	
#
#   Get sensor by id
#
@sensors_bp.route('/<int:sensor_id>', methods = ['GET'])
def get_sensor(sensor_id):
	# Retrieve data for sensor id
	sensor_data = sensors_services.get_sensor_data_by_id(sensor_id)

	# Verify if data exists
	if sensor_data is None:
		return jsonify({"status": "error", 
						"message": f"No data found for id: {sensor_id}"}), HTTPStatus.NOT_FOUND

	return jsonify(sensor_data), HTTPStatus.OK

#
#   Add sensor
#
@sensors_bp.route('', methods = ['POST'])
def add_sensor():
	# Get JSON data from request
	sensor_data = request.json
	print(f"JSON Data: \n{sensor_data}")
	
	# Send data to service layer
	sensors_services.add_sensor(sensor_data)

	return jsonify({"status": "success", 
					"message": "Sensor added successfully."}), HTTPStatus.OK

#
#   Update
#
@sensors_bp.route('/<int:sensor_id>', methods = ['PUT'])
def update_sensor(sensor_id):
	# Check if sensor id is valid
	if sensors_services.get_sensor_data_by_id(sensor_id) is None:
		return jsonify({"status": "error", 
						"message": f"No data found for id: {sensor_id}"}), HTTPStatus.NOT_FOUND

	# Get JSON updated data
	sensor_data = request.json

	# Call service function for update
	sensors_services.update_sensor_by_id(sensor_id, sensor_data)

	return jsonify({"status": "success", 
					"message": f"Sensor with id: {sensor_id} updated successfully."}), HTTPStatus.OK

#
#   Delete sensor by id
#
@sensors_bp.route('/<int:sensor_id>', methods = ['DELETE'])
def detele_sensor(sensor_id):
	# Retrieve data for sensor id
	sensor_data = sensors_services.get_sensor_data_by_id(sensor_id)

	if sensor_data is None:
		return jsonify({"status": "error", "message": 
						f"No data found for id: {sensor_id}"}), HTTPStatus.NOT_FOUND

	# Call service function for delete
	sensors_services.detele_sensor_by_id(sensor_id), 200
	
	return jsonify({"status" : "success",
					"message" : f"Successfully deleted sensor with id: {sensor_id}"}), HTTPStatus.OK
