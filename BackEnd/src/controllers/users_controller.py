from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.services.users_service import *

####################
#
#   Add the path to the project
#
####################
import sys
sys.path.append("src")


USERS_URL = '/api/users'

#
#   Setup Blueprint
#
users_bp = Blueprint('users', __name__, url_prefix= USERS_URL)

####################
# 
#   Routes
#
####################

#
#	Fetch all users
#
@users_bp.route('', methods=['GET'])
def get_users() -> jsonify:
	
	# Service response
	response = get_users_data()

	if response is None:
		return jsonify({"status:": "error",
						"message": "No users available"}), HTTPStatus.NOT_FOUND
	
	return jsonify(response), HTTPStatus.OK


#
#   Create User
#
@users_bp.route('', methods=['POST'])
def add_user() -> jsonify:
	# Fetch JSON
	user_data = request.get_json()

	try:
		# Create User object from dict
		user = User.from_dict(user_data)

		# Service response
		response = create_user(user)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.CREATED
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	

#
#	Update User
#
@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id: str) -> jsonify:
	# Fetch JSON
	user_data = request.get_json()

	try:
		# Retrieve attributes
		user_email =  user_data["email"]
		user_password = user_data["password"]

		# Create User object
		user_obj = User(email=user_email, password=user_password)

		# Service response
		response = update_user_by_id(user_id, user_obj)

		if "error" in response:
			return jsonify({"status": "error", 
					"error": response["error"]}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK
	
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
	

#	
#	Delete User by ID
#
@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id: str) -> jsonify:

	try:
		# Service response
		response = delete_user_by_id(user_id)

		if "error" in response:
			return jsonify({"status": "error",
							"message": response["error"]}), HTTPStatus.BAD_REQUEST
		
		return jsonify(f"Deleted user: {response}"), HTTPStatus.OK
		
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
