from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.classes.UserAlerts import UserAlerts
from src.services.alerts_service import create_alert

ALERTS_URL = '/api/alerts'

#
#   Setup Blueprint
#
alerts_bp = Blueprint('alerts', __name__, url_prefix= ALERTS_URL)

####################
# 
#   Routes
#
####################

#
#   Create alert
#
@alerts_bp.route('', methods=['POST'])
def add_alert() -> jsonify:
	data = request.get_json()
	try:
		alert = UserAlerts.from_dict(data)

		# Service response
		response = create_alert(alert)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST
	
		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR