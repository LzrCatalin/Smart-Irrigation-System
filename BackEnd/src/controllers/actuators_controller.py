import logging

from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.services.actuators_service import toggle_water_pump
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