from flask import Flask, jsonify, request
from http import HTTPStatus

####################
#
#   Add the path to the project
#
####################
import sys
sys.path.append("src")

from src.firebase.services import sensors_services
from src.classes.Sensor import Sensor
from src.sensors.testFunctions import *

SENSORS_URL = '/api/sensors'

###################
#
#   Controller function
#
###################
def create_sensors_controller(app: Flask):
	#
	#   Get sensors
	#
	@app.route(f'{SENSORS_URL}', methods = ['GET'])
	def get_sensors():
		# Retrieve sensors data
		sensors_data = sensors_services.get_sensors_data()
		
		# Verify if data exists
		if sensors_data == HTTPStatus.NOT_FOUND:
			return jsonify({"status:": "error",
							"message": "No sensors available"}), HTTPStatus.NOT_FOUND
		
		return jsonify(sensors_data), HTTPStatus.OK
		
	#
	#   Get sensor by id
	#
	@app.route(f'{SENSORS_URL}/<int:sensor_id>', methods = ['GET'])
	def get_sensor(sensor_id):
		# Retrieve data for sensor id
		sensor_data = sensors_services.get_sensor_data(sensor_id)

		# Verify if data exists
		if sensor_data == HTTPStatus.NOT_FOUND:
			return jsonify({"status": "error", 
							"message": f"No data found for id: {sensor_id}"}), HTTPStatus.NOT_FOUND

		return jsonify(sensor_data), HTTPStatus.OK

	#
	#   Add sensor
	#
	@app.route(f'{SENSORS_URL}', methods = ['POST'])
	def add_sensor():
		# Get JSON data from request
		sensor_data = request.json
		print(f"JSON Data: \n{sensor_data}")

		"""
			Created two function to simulate humidity and temperature
			received from a sensor and use it to push the sensor
			into db

			After, those function will be changed with initial sensor 
			functions
		"""
		# Create Sensor object
		sensor = Sensor(
			name = sensor_data['sensor_name'],
			temperature = calculate_temperature_percentage(),
			humidity = calculate_moisture_percentage()
		)

		# Call service function for add
		sensors_services.add_sensor(sensor)

		return jsonify({"status": "success", 
						"message": "Sensor added successfully."}), HTTPStatus.OK

	#
	#   Update
	#
	@app.route(f'{SENSORS_URL}/<int:sensor_id>', methods = ['PUT'])
	def update_sensor(sensor_id):
		# CHeck if sensor id is valid
		if sensors_services.get_sensor_data(sensor_id) == HTTPStatus.NOT_FOUND:
			return jsonify({"status": "error", 
							"message": f"No data found for id: {sensor_id}"}), HTTPStatus.NOT_FOUND

		# Get JSON updated data
		sensor_data = request.json

		# Create Sensor object
		sensor = Sensor(
			name = sensor_data['sensor_name'],
			temperature = calculate_temperature_percentage(),
			humidity = calculate_moisture_percentage()
		)

		# Call service function for update
		sensors_services.update_sensor_by_id(sensor_id, sensor)

		return jsonify({"status": "success", 
						"message": f"Sensor with id: {sensor_id} updated successfully."}), HTTPStatus.OK

	#
	#   Delete sensor by id
	#
	@app.route(f'{SENSORS_URL}/<int:sensor_id>', methods = ['DELETE'])
	def detele_sensor(sensor_id):
		# Retrieve data for sensor id
		sensor_data = sensors_services.get_sensor_data(sensor_id)

		if sensor_data == HTTPStatus.NOT_FOUND:
			return jsonify({"status": "error", "message": 
							f"No data found for id: {sensor_id}"}), HTTPStatus.NOT_FOUND

		# Call service function for delete
		sensors_services.detele_sensor_by_id(sensor_id), 200
		
		return jsonify({"status" : "success",
						"message" : f"Successfully deleted sensor with id: {sensor_id}"}), HTTPStatus.OK