import logging

from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.actuators.water_pump import pump_start, pump_stop

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