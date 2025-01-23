import logging
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
