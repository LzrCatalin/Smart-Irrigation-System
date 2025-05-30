import logging
import requests
from colorama import Fore, Style

from src.classes.Status import Status
from src.classes.Field import Field
from src.classes.FieldDTO import FieldDTO
from src.classes.AlertDefinition import AlertDefinition
from src.services.alerts_service import create_alert
from src.services.sensors_services import set_available_status, set_not_available_status, get_sensor_by_name, get_sensor_data_by_id, update_sensor_by_id, set_sensor_field_id, unset_sensor_field_id
from src.services.users_service import get_user_by_id
from src.util.soil_fetch import get_soil_info

from firebase_admin import credentials, db
from src.util.mail_sender import  send_email, generate_field_creation_email_body, generate_field_update_mail_body, generate_field_delete_mail_body
from src.api.geocodinAPI import get_location

#######################
#
#   Database path for users
#
#######################
DB_REF = 'irrigation-system/field_data'
REF = db.reference(f'{DB_REF}')

#######################
#
#	Fetch db methods
#
#######################

#
#	Fetch fields from db
#
def get_fields_data() -> dict:

	try:	
		# Fetch db
		fields_ref = REF.get()
		return fields_ref
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

#
#	Fetch fields with placed sensors 
#
def get_fields_with_sensors() -> dict:

	try:
		fields_data = get_fields_data()

		# Filter
		fields_with_sensors = {
			field_id: field
			for field_id, field in fields_data.items()
			if "sensors" in field and field["sensors"]
		}

		return fields_with_sensors

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#
#	Fetch all field ids from db
#
def get_field_ids() -> list[str]:
	fields_data = REF.get()

	return list(fields_data.keys() if fields_data else [])

#
#	Fetch all fields ids with sensors
#
def get_field_ids_with_sensors() -> list[str]:
	fields_data = REF.get()

	if not fields_data:
		return []

	return [
		field_id
		for field_id, field in fields_data.items()
		if 'sensors' in field and field['sensors']
	]

#
#	Fetch field by ID
#
def get_field_by_id(id: str) -> dict:

	# Fetch
	field_ref = REF.child(id).get()

	# Check existance
	if field_ref is None:
		return {"error": f"No data found for ID: {id}"}
	
	try:
		
		# Field object
		field = Field.from_dict(field_ref)

		# FieldDTO convert
		field_dto = FieldDTO(id=id, 
					latitude= field.latitude, longitude= field.longitude,
					width= field.width, length= field.length, slope= field.slope,
					user= field.user,
					soil_type= field.soil_type, crop_name= field.crop_name,
					sensors= [sensor.to_dict() for sensor in field.sensors])
		
		return field_dto.to_dict()
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Fetch fields by user email
#
def get_fields_by_user_id(user_id: str) -> list[dict]:

	# Fetch data
	fields_ref = REF.order_by_child('user').equal_to(user_id).get()
	logging.debug(f"Fetched fields: {fields_ref}")

	# Check fetch response
	if fields_ref is None:
		return [{"error": f"No fields for user: {user_id}"}]
	
	try:
		# Create fieldDTO obj array
		fields_dtos = [
			FieldDTO(
				id=field_id,
				**Field.from_dict(field_data).to_dict()
			).to_dict()
			for field_id, field_data in fields_ref.items()
		]

		return fields_dtos


	except KeyError as e:
		return [{"error": f"Key missing: {str(e)}"}]

#
#	Fetch field's user
#
def get_field_user(field_id: str) -> str:
	field_data = get_field_by_id(field_id)
	return field_data['user']

#
#	Fetch field's location
#
def get_location_by_field_id(field_id: str) -> str:

	# Verify field id
	field_data = get_field_by_id(field_id)

	# Return the location
	return (get_location(field_data['latitude'], field_data['longitude']))

#######################
#
#   CRUD Operations
#
#######################

#
#   Create
#
def create_field(data: Field, sensors_ids: list[str]) -> dict:	
	try:
		# Fetch soil type based on longitude and longitude
		data.soil_type = get_soil_info(data.latitude, data.longitude)

		# Retrieve user data for mail sender
		user_data = get_user_by_id(data.user)
		
		# Push the field into db
		field_ref = REF.push(data.to_dict())

		# Check if there are selected sensors
		if not sensors_ids:
			data.sensors = []
		
		else:
			# Update selected sensors status and field id
			for id in sensors_ids:
				# Update status and field id
				set_not_available_status(id)
				set_sensor_field_id(id, field_ref.key)

		# Create DTO object
		field_dto = FieldDTO(
			id = field_ref.key,
			latitude = data.latitude,
			longitude = data.longitude,
			length = data.length,
			width = data.width,
			slope = data.slope,
			soil_type = data.soil_type,
			crop_name = data.crop_name,
			user = data.user,
			sensors = [sensor.to_dict() for sensor in data.sensors or []],
		)	

		# Send Mail
		send_email("Your New Field Has Been Successfully Added",
			 		generate_field_creation_email_body(
						user_data['email'],
						get_location(data.latitude, data.longitude)[8:],
						field_dto
					),
					user_data['email'])
		
		# Create the alert
		alert_def = AlertDefinition(
			user_id=user_data['id'],
			message="Your New Field Has Been Successfully Added",
			alert_type="INFO"
		)
		create_alert(alert_def)

		logging.info(Fore.GREEN + 
				"Successfully added new field." +
				Style.RESET_ALL)
		
		return field_dto.to_dict()
		
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Update field by ID
#
def update_field_by_id(id: str, data: Field, deleted_data: dict) -> dict:
	# Check ID
	get_field_by_id(id) 

	try:
		
		# Check if exists deleted sensors from update request
		if deleted_data:
			for sensor_data in deleted_data['deleted_sensors']:
				# Set AVAILABLE status for deleted sensor
				set_available_status(sensor_data['name'])
				unset_sensor_field_id(sensor_data['name'])

		# Fetch new list of sensors from the update request
		selected_sensors = data.to_dict()['sensors']

		# Check if exists
		if selected_sensors:
			for sensor_data in selected_sensors:
				# Set NOT_AVAILABLE status for selected sensor
				sensor = get_sensor_by_name(sensor_data['name'])
				set_not_available_status(sensor['firebase_id'])
				set_sensor_field_id(sensor['firebase_id'], id)

		# Create DTO object
		updated_field_dto = FieldDTO(
			id = id,
			latitude = data.latitude,
			longitude = data.longitude,
			length = data.length,
			width = data.width,
			slope = data.slope,
			soil_type = data.soil_type,
			crop_name = data.crop_name,
			user = data.user,
			sensors = [sensor.to_dict() for sensor in data.sensors],
		)
		
		# Update DB
		REF.child(id).set(data.to_dict())

		# Retrieve user data for mail sender
		user_data = get_user_by_id(updated_field_dto.user)

		# Send Mail
		send_email(f"Field Updated: {updated_field_dto.crop_name} at {get_location(updated_field_dto.latitude, updated_field_dto.longitude)[8:]}",
			 		generate_field_update_mail_body(
						user_data['email'],
						get_location(updated_field_dto.latitude, updated_field_dto.longitude)[8:],
						updated_field_dto
					),
					user_data['email'])
		
		logging.info(Fore.GREEN + 
				f"Successfully updated field data for ID: {id}" + 
				Style.RESET_ALL)
		
		return updated_field_dto.to_dict()
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
#
#	Update field measurement
#
def update_field_measurements_by_id(id: str, data: Field) -> dict:

	try:
		# Create DTO object
		updated_field_dto = FieldDTO(
			id = id,
			latitude = data.latitude,
			longitude = data.longitude,
			length = data.length,
			width = data.width,
			slope = data.slope,
			soil_type = data.soil_type,
			crop_name = data.crop_name,
			user = data.user,
			sensors = [sensor.to_dict() for sensor in data.sensors],
		)
		
		# Update DB
		REF.child(id).set(data.to_dict())

		# Retrieve user data for mail sender
		user_data = get_user_by_id(updated_field_dto.user)

			 		
		# Send Mail
		send_email("Field Updated",
			 		f"Successfully updated measurements on location {get_location(updated_field_dto.latitude, updated_field_dto.longitude)}",
					user_data['email'])
		
		logging.info(Fore.GREEN + 
				f"Successfully updated field measurements for ID: {id}" + 
				Style.RESET_ALL)
		
		return updated_field_dto.to_dict()
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
		
#
#	Delete field by ID
#
def delete_field_by_id(id: str, sensors_names: list[str]) -> dict:

	try:
		# Check ID
		fetched_field = get_field_by_id(id)

		# Fetch user by id
		user_data = get_user_by_id(fetched_field['user'])

		# Check for sensors
		if sensors_names:
			for name in sensors_names:
				# Update sensor status
				set_available_status(name)
				unset_sensor_field_id(name)

		# Send Mail
		send_email(f"Field Deleted: {fetched_field['crop_name']} at {get_location(fetched_field['latitude'], fetched_field['longitude'])[8:]}",
			 		generate_field_delete_mail_body(
						user_data['email'],
						get_location(fetched_field['latitude'], fetched_field['longitude'])[8:],
						fetched_field['crop_name']
					),
					user_data['email'])
		
		# Delete 
		REF.child(id).delete()
		
		logging.info(Fore.GREEN + 
					f"Successfully delete data for field ID: {id}" +
					Style.RESET_ALL)
		
		return fetched_field

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
		


