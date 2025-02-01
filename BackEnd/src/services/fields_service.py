import logging
import requests
from colorama import Fore, Style
from src.classes.Field import *
from src.classes.FieldDTO import *
from firebase_admin import credentials, db

#######################
#
#   Database path for users
#
#######################
DB_REF = 'irrigation-system/field_data'
REF = db.reference(f'{DB_REF}')


####################
#
#	Util functions
#
####################
def get_soil_type(latitude: float, longitude: float) -> str:
	logging.debug(f"\t\tRetrieving soil type: {longitude} : {latitude}")

	# SoilGrids API endpoint
	url = f"https://rest.isric.org/soilgrids/v2.0/classification/query?lon={longitude}&lat={latitude}"

	# Make the request
	response = requests.get(url)
	logging.debug(f"URL RESPONSE: {response.status_code}")

	if response.status_code == 200:
		data = response.json()
		logging.debug(f"DATA RESPONSE: {data}")

		# Extract the soil type from the correct key
		soil_type = data.get('wrb_class_name', 'Unknown')
		logging.debug(f"Successfully fetched soil type: {soil_type}")
		return soil_type
	else:
		logging.debug("ERROR")
		logging.error(f"Error: {response.status_code} - {response.text}")
		return None
	

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
		fieldDTO = FieldDTO(id=id, 
					latitude= field.latitude, longitude= field.longitude,
					width= field.width, length= field.length, slope= field.slope,
					user= field.user,
					soil_type= field.soil_type, crop_name= field.crop_name,
					sensors= [sensor.to_dict() for sensor in field.sensors])
		
		return fieldDTO.to_dict()
	
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
		return {"error": f"No fields for user: {user_id}"}
	
	try:
		# Create fieldDTO obj array
		fieldsDTOs = [
			FieldDTO(
				id = field_id,
				**Field.from_dict(field_data).to_dict()
			).to_dict()

			for field_id, field_data in fields_ref.items()
		]

		return fieldsDTOs


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
def create_field(data: Field) -> dict:
	
	try:
		# Fetch soil type based on longitude and longitude
		data.soil_type = get_soil_type(data.longitude, data.latitude)
		logging.debug(f"Fetched soil type: {data.soil_type}")

		# Push the field into db
		field_ref = REF.push(data.to_dict())

		# Create DTO object
		fieldDTO = FieldDTO(
			id = field_ref.key,
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

		logging.info(Fore.GREEN + 
				"Successfully added new user." +
				Style.RESET_ALL)
		
		return fieldDTO.to_dict()
		
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}


#
#	Update field by ID
#
def update_field_by_id(id: str, data: Field) -> dict:
	# Check ID
	get_field_by_id(id)

	try:
		# Update DB
		REF.child(id).set(data.to_dict())

		# Create DTO object
		updated_fieldDTO = FieldDTO(
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

		logging.info(Fore.GREEN + 
				f"Successfully updated field data for ID: {id}" + 
				Style.RESET_ALL)
		
		return updated_fieldDTO.to_dict()
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	

#
#	Delete field by ID
#
def delete_field_by_id(id: str) -> dict:

	try:
		# Check ID
		fetched_field = get_field_by_id(id)

		# Delete 
		REF.child(id).delete()

		logging.info(Fore.GREEN + 
					f"Successfully delete data for field ID: {id}" +
					Style.RESET_ALL)
		
		return fetched_field

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
		


