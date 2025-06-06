from http import HTTPStatus
from flask import jsonify, request, Blueprint

from services.irrigation_config_service import push_into_system, remove_from_system
from services.irrigation_config_service import update_field_irrigation_config
from services.irrigation_config_service import toggle_irrigation_activity, toggle_scheduler_activity
from services.irrigation_config_service import update_irrigation_interval, update_sensors_interval

SYSTEM_URL = '/api/system'

#
#   Setup Blueprint
#
system_bp = Blueprint('system',  __name__, url_prefix= SYSTEM_URL)

####################
# 
#   Routes
#
####################
@system_bp.route('/<field_id>', methods=['POST'])
def add_into_system(field_id: str) -> jsonify:
	try:
		# Service response
		response = push_into_system(field_id)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@system_bp.route('/<field_id>', methods=['DELETE'])
def delete_from_system(field_id: str) -> jsonify:
	try:
		# Service response
		response = remove_from_system(field_id)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
@system_bp.route('/field_config', methods=['PUT'])
def update_field_config() -> jsonify:
	try:
		# Fetch data
		data = request.get_json()

		# Service response
		response = update_field_irrigation_config(data)

		return jsonify(response)
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@system_bp.route('/scheduler/toggle', methods=['POST'])
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
	
@system_bp.route('/irrigation/toggle', methods=['POST'])
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
		
@system_bp.route('/scheduler/updated_timer', methods=['POST'])
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
		
@system_bp.route('/irrigation/updated_timer', methods=['POST'])
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