import logging

from src.util.utils import alert
from src.actuators.water_pump import pump_start, pump_stop
from src.services.fields_service import get_field_ids
from src.services.history_service import add_irrigation
from src.api.geocodinAPI import get_location_by_field_id

####################
#
#	Util functions
#
####################
def toggle_water_pump(data: dict) -> dict:
	try:
		# Extract state
		state = data['state']
		user_id = data['user_id']
		field_id = data['field_id']

		if state == 1:
			pump_start()

			# Irrigate selected field
			add_irrigation(field_id)

			# Fetch field location
			location = get_location_by_field_id(field_id)

			# Send alert
			alert(
				user_id=user_id,
		 		message=f"Water Pump manually activated for {location[8:]}",
				type="INFO"
			)

			return {"message": "WATER PUMP -> ON"}
		
		pump_stop()

		# Send alert
		alert(
			user_id=user_id,
			message="Water Pump manually stopped.",
			type="INFO"
		)

		return {"message": "WATER PUMP -> OFF"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	