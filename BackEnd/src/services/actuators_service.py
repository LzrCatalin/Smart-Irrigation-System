import logging

from src.util.utils import alert
from src.actuators.water_pump import pump_start, pump_stop
from src.services.fields_service import get_field_ids
from src.services.history_service import add_irrigation

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

		if state == 1:
			pump_start()

			# Fetch all field ids
			field_ids = get_field_ids()
			for id in field_ids:
				# Add irrigation history
				add_irrigation(id)

			# Send alert
			alert(
				user_id=user_id,
		 		message="Water Pump manually activated.",
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
	