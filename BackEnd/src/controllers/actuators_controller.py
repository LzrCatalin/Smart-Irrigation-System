import logging

from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.services.actuators_service import toggle_water_pump, toggle_scheduler_activity, toggle_irrigation_activity, update_sensors_interval, update_irrigation_interval
from src.services.actuators_service import update_field_irrigation_config

ACTUATORS_URL = '/api/actuators'

#
#   Setup Blueprint
#
actuators_bp = Blueprint('actuators', __name__, url_prefix= ACTUATORS_URL)

####################
# 
#   Routes
#
####################
@actuators_bp.route('/waterpump/toggle', methods=['POST'])
def get_toggle_state() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()
		
		# Service response
		response = toggle_water_pump(data)

		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
@actuators_bp.route('/scheduler/toggle', methods=['POST'])
def get_scheduler_state() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()

		# Service response
		response = toggle_scheduler_activity(data)
		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
@actuators_bp.route('/irrigation/toggle', methods=['POST'])
def get_irrigation_state() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()

		# Service response
		response = toggle_irrigation_activity(data)
		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
		
@actuators_bp.route('/scheduler/updated_timer', methods=['POST'])
def update_scheduler_settings() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()

		# Service response
		response = update_sensors_interval(data)
		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
		
@actuators_bp.route('/irrigation/updated_timer', methods=['POST'])
def update_irrigation_settings() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()

		# Service response
		response = update_irrigation_interval(data)
		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@actuators_bp.route('/field_config', methods=['PUT'])
def update_field_config() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()

		# Service response
		response = update_field_irrigation_config(data)

		return jsonify(response)
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
