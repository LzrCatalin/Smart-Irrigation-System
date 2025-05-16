from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.services.history_service import get_field_history, add_irrigation

IRRIGATIONS_URL = '/api/history'

#
#   Setup Blueprint
#
irrigations_bp = Blueprint('history', __name__, url_prefix= IRRIGATIONS_URL)

####################
# 
#   Fetches
#
####################
@irrigations_bp.route('/<field_id>', methods=['GET'])
def fetch_field_history(field_id: str) -> jsonify:
	try:
		# Service response
		field_history = get_field_history(field_id)

		if field_history is None:
			return jsonify({
				"status": "error",
				"message": "No history found for the field."
			}), HTTPStatus.NOT_FOUND
		
		return jsonify(field_history.to_dict()), HTTPStatus.OK

	except Exception as e:
		return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	
####################
# 
#   Routes
#
####################

#
#	Add to history
#
@irrigations_bp.route('/<field_id>', methods=['POST'])
def create(field_id: str) -> jsonify:
	try:
		# Service response
		response = add_irrigation(field_id)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST
	
		return jsonify(response), HTTPStatus.OK
		
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR