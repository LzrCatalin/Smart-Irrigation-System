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
from src.classes.SensorType import *
from src.sensors.humidity_sensor import *

SENSORS_URL = '/api/sensors'

#
#   Setup Blueprint
#
sensors_bp = Blueprint('sensors', __name__, url_prefix= SENSORS_URL)

#
#   Get sensors
#
@sensors_bp.route('', methods = ['GET'])
def get_sensors() -> jsonify:
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
@sensors_bp.route('/<sensor_id>', methods = ['GET'])
def get_sensor(sensor_id) -> jsonify: 
	logging.debug("Calling route ---> get_sensor -> by id")

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
def add_sensor() -> jsonify:
	# Get JSON data from request
	sensor_data = request.json
	print(f"JSON Data: \n{sensor_data}")
	
	try:
		# Convert JSON data to Sensor object
		sensor = Sensor.from_dict(sensor_data)

		# Send data to service layer
		response = sensors_services.add_sensor(sensor)

		if response is "error":
			return jsonify({"status": "failure", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify({"status": "success", 
						"message": f"Sensor added successfully.{response}"}), HTTPStatus.OK

	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

#	
#   Update
#
@sensors_bp.route('/<sensor_id>', methods = ['PUT'])
def update_sensor(sensor_id) -> jsonify:

	try:
		data = request.get_json()	

		# Extract fields for SensorType
		sensor_type = SensorType(
			type = data['type']['type'],
			measured_value = data['type']['measured_value'],
			status = data['type']['status'],
			port = data['type']['port']
		)
		
		# Create the Sensor object
		sensor = Sensor(
			name = data['name'],
			type = sensor_type
		)
	
		# Call service function for update
		sensor = sensors_services.update_sensor_by_id(sensor_id, sensor)

		if "error" in sensor:
			return jsonify({"status": "error", 
				   "message": sensor["error"]}), HTTPStatus.BAD_REQUEST

		
		return jsonify({"status": "success", 
						"message": f"{sensor}"}), HTTPStatus.OK
	
	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

#
#   Delete sensor by id
#
@sensors_bp.route('/<sensor_id>', methods = ['DELETE'])
def detele_sensor(sensor_id) -> jsonify:
	try:
		# Call service function for delete
		sensor = sensors_services.detele_sensor_by_id(sensor_id)
		
		if "error" in sensor:
			return jsonify({"status": "error",
							"message": sensor["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify({"status" : "success",
						"message" : f"Successfully deleted sensor with id: {sensor_id}"}), HTTPStatus.OK
	
	except Exception as e:
		# Catch unexpected errors
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
