import logging
from colorama import Fore, Style
from src.util.encrypt import *
from src.classes.User import *
from src.classes.UserDTO import *
from src.firebase.db_init import db_init
from firebase_admin import credentials, db
#######################
#
#   Database path for users
#
#######################
DB_REF = 'irrigation-system/user_data'
REF = db.reference(f'{DB_REF}')

#######################
#
#	Fetch db methods
#
#######################


#
#	Fetch users from db
#
def get_users_data() -> list[dict]:
	try:
		# Fetch users data from db
		users_ref = REF.get()
		return users_ref

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Fetch user by ID
#
def get_user_by_id(id: str) -> dict:

	# Fetch data from db
	user_ref = REF.child(id).get()

	# Check existance
	if user_ref is None:
		return {"error": f"No data found for ID: {id}"}

	try:
		# UserDTO convert
		userDTO = UserDTO(id=id, email = user_ref["email"])

		# Return dict of extracted data
		return userDTO.to_dict()

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Check email in DB
#
def available_email(email: str) -> bool:
	
	try:
		# Fetch data from db
		users_ref = REF.get()

		# Check existance
		if users_ref:
			for _, user_data in users_ref.items():
				if user_data.get('email') == email:
					return False
		
		return True
			
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}



#
#	Fetch user by email
#
def get_user_by_email(email: str) -> dict:
	
	try:
		# Fetch DB
		user = REF.order_by_child('email').equal_to(email).get()

		if not user:
			return {"error": f"No user found for email: {email}"}
		
		for user_id, user_data in user.items():
			return UserDTO(user_id, user_data["email"]).to_dict()
		
		return {"error": "Unexpected error."}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Fetch user by email and password
#
def get_user_by_email_and_password(email: str, password: str) -> dict:

	try:
		# Fetch DB by email
		user_ref = REF.order_by_child('email').equal_to(email).get()

		if user_ref is None:
			return {"error": f"No user found with email: {email}"}

		# Verify email and password
		for user_id, user_data in user_ref.items():

			if user_data["password"] == password:
				return UserDTO(user_id, email).to_dict()

		return {"error": "Invalid password or email."}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#######################
#
#   CRUD Operations
#
#######################


#
#   Create
#
def create_user(data: User) -> dict:

	try:
		# Retrieve attributes
		email = data.email
		password = data.password

		#
		#	Check if email is available
		#
		if available_email(email):
			# Create the new user with encrypted password
			created_user = User(email=email, password=encrypt(password))
			
			# Push the user into db
			user_ref = REF.push(created_user.to_dict())

			# Create DTO object
			userDTO = UserDTO(id=user_ref.key, email=data.email)
			
			logging.info(Fore.GREEN + 
				"Successfully added new user." +
				Style.RESET_ALL)
			
			return userDTO.to_dict()
		
		else:
			return {"error": f"Email: {email} already in use."}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	

#
#	Update User by ID
#
def update_user_by_id(id: str, data: User) -> dict:

	try:
		# Fetch user by ID
		user = get_user_by_id(id)

		# Verify new email availability
		available_email(user["email"])

		# Update the user
		new_user = User(data.email, encrypt(data.password))

		# Push new data
		REF.child(id).set(new_user.to_dict())

		logging.info(Fore.GREEN + 
			   f"Successfully updated user data for ID: {id}" + 
			   Style.RESET_ALL)
		
		# Create userDTO obj
		userDTO = UserDTO(id, data.email)
		return userDTO.to_dict()
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Delete user
#
def delete_user_by_id(id: str) -> dict:

	try:
		# Fetch user by ID
		user = get_user_by_id(id)

		# Delete 
		REF.child(id).delete()

		logging.info(Fore.GREEN + 
					f"Successfully delete data for user ID: {id}" +
					Style.RESET_ALL)
		
		return user
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}