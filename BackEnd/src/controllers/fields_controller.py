from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.services.fields_service import *

FIELDS_URL = '/api/fields'

#
#   Setup Blueprint
#
fields_bp = Blueprint('fields', __name__, url_prefix= FIELDS_URL)


####################
# 
#   Routes
#
####################

#
#   Fetch all fields
#
@fields_bp.route('', methods= ['GET'])
def get_fields() -> jsonify:


	# Service response
	response = get_fields_data()

	if response is None:
		return jsonify({"status:": "error",
						"message": "No fields available"}), HTTPStatus.NOT_FOUND
	
	return jsonify(response), HTTPStatus.OK


#
#	Fetch field by ID
#
@fields_bp.route('/<field_id>', methods= ['GET'])
def get_field(field_id: str) -> jsonify:

	# Service response
	response = get_field_by_id(field_id)

	if "error" in response:
		return jsonify({"status": "error",
						"error": response["error"]}), HTTPStatus.BAD_REQUEST
	
	return jsonify(response), HTTPStatus.OK


#
#	Fetch fields by user email
#
@fields_bp.route('/all/<user_id>', methods= ['GET'])
def get_user_fields(user_id: str) -> jsonify:

	# Service response
	response = get_fields_by_user_id(user_id)

	if "error" in response:
		return jsonify({"status": "error",
				 		"error": response["error"]}), HTTPStatus.BAD_REQUEST
	
	return jsonify(response), HTTPStatus.OK


#
#	Create fields
#
@fields_bp.route('', methods=['POST'])
def add_field() -> jsonify:
	# Fetch JSON
	field_data = request.get_json()
	logging.debug(f"\t\t FIELD CONTROLLER : Received data: {field_data}")

	try:
		# Retrieve sensors ids from JSON
		sensors_ids = []
		sensors_data = field_data['sensors']
		for data in sensors_data:
			sensors_ids.append(data['id'])

		# Create Field object 
		field = Field.from_dict(field_data)

		# Service response
		response = create_field(field, sensors_ids)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify(response), HTTPStatus.CREATED

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	

#
#	Update field
#
@fields_bp.route('/<field_id>', methods=['PUT'])
def update_field(field_id: str) -> jsonify:
	# Fetch JSON 
	data = request.get_json()
	logging.debug(f"Received data: {data}")
	logging.debug(f"New Field data: {data['field_data']}")
	logging.debug(f"Deleted sensors: {data['deleted_data']}")

	try:
		# Create Field object
		field = Field.from_dict(data['field_data'])
		deleted_sensors = data['deleted_data']

		# Service response
		response = update_field_by_id(field_id, field, deleted_sensors)

		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify("ok"), HTTPStatus.OK

	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


#
#	Delete field
#
@fields_bp.route('/<field_id>', methods=['DELETE'])
def delete_field(field_id: str) -> jsonify:
	
	data = request.get_json()
	logging.debug(f"Received sensors: {data}")
	
	try:
		# Fetch sensors from JSON
		field_sensors = data["sensors_name"]

		# Service response
		response = delete_field_by_id(field_id, field_sensors)

		if "error" in response:
			return jsonify({"status": "error",
				   			"error": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	