import logging

from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.actuators.water_pump import pump_start, pump_stop
from src.util.extensions import get_sensors_scheduler, get_irrigation_system

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
		data = request.get_json()
		# Retrieve value 
		toggle = data['state']

		if toggle == 1:
			pump_start()
			return jsonify({"message": "WATER PUMP -> ON"}), HTTPStatus.OK
		
		pump_stop()
		return jsonify({"message": "WATER PUMP -> OFF"}), HTTPStatus.OK


	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
@actuators_bp.route('/scheduler/toggle', methods=['POST'])
def get_scheduler_state() -> jsonify:
	try:
		data = request.get_json()

		scheduler = get_sensors_scheduler()
		if not scheduler:
			return jsonify({"status": "error", "message": "Scheduler not initialized"}), HTTPStatus.INTERNAL_SERVER_ERROR

		toggle_state = data['state']
		if toggle_state == 1:
			scheduler.pause_sensor_updates()
			print('Scheduler -> PAUSED')
			return jsonify({"message": "Scheduler paused"}), HTTPStatus.OK

		scheduler.resume_sensor_updates()
		print('Scheduler -> RESUMED')
		return jsonify({"message": "Scheduler resumed"}), HTTPStatus.OK

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
@actuators_bp.route('/irrigation/toggle', methods=['POST'])
def get_irrigation_state() -> jsonify:
	try:
		data = request.get_json()

		irrigation = get_irrigation_system()
		if not irrigation:
			return jsonify({"status": "error", "message": "Irrigation not initialized"}), HTTPStatus.INTERNAL_SERVER_ERROR
		
		toggle_state = data['state']
		if toggle_state == 1:
			irrigation.pause_irrigation_system()
			print('Irrigation -> PAUSED')
			return jsonify({"message": "Irrigation paused"}), HTTPStatus.OK

		irrigation.resume_irrigation_system()
		print('Irrigation -> RESUMED')
		return jsonify({"message": "Irrigation resumed"}), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
		
