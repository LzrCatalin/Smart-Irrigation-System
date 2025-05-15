from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.classes.UserAlerts import UserAlerts
from src.services.alerts_service import create_alert, get_user_alerts

ALERTS_URL = '/api/alerts'

#
#   Setup Blueprint
#
alerts_bp = Blueprint('alerts', __name__, url_prefix= ALERTS_URL)

####################
# 
#   Fetches
#
####################
@alerts_bp.route('/<user_id>', methods=['GET'])
def fetch_user_alerts(user_id: str) -> jsonify:
	try:
		# Service response
		user_alerts = get_user_alerts(user_id)

		if user_alerts is None:
			return jsonify({
				"status": "error",
				"message": "No alerts found or user does not exist."
			}), HTTPStatus.NOT_FOUND

		return jsonify(user_alerts.to_dict()), HTTPStatus.OK

	except Exception as e:
		return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

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