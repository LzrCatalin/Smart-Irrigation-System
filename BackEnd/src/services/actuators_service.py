import logging

from src.util.utils import alert
from src.actuators.water_pump import pump_start, pump_stop
from src.util.extensions import get_sensors_scheduler, get_irrigation_system

from src.api.geocodinAPI import get_location
from src.util.mail_sender import  send_email, generate_field_config_update
from src.services.fields_service import get_field_by_id, get_field_ids
from src.services.users_service import get_user_by_id
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

def toggle_scheduler_activity(data: dict) -> dict:
	try:
		# Extract state
		state = data['state']
		user_id = data['user_id']
		
		# Get job
		scheduler = get_sensors_scheduler()
		if not scheduler:
			# Send alert
			alert(
				user_id=user_id,
				message="No job for updates found.",
				type="WARNING"
			)
		
			return {"error": "Scheduler not initialized"}

		# Make decision
		if state == 1:
			scheduler.pause_sensor_updates()
			alert(
				user_id=user_id,
				message="Paused sensor updates.",
				type="INFO"
			)

			return {"message": "Scheduler paused"}

		# Turn ON updates + send alert
		scheduler.resume_sensor_updates()
		alert(
			user_id=user_id,
			message="Resumed sensor updates.",
			type="INFO"
		)
		
		return {"message": "Scheduler resumed"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
def toggle_irrigation_activity(data: dict) -> dict:
	try:
		# Extract state
		state = data['state']
		user_id = data['user_id']

		# Get job
		irrigation = get_irrigation_system()
		if not irrigation:
			# Send alert
			alert(
				user_id=user_id,
				message="No job found for irrigation.",
				type="WARNING"
			)
			return {"error": "Irrigation not initialized"}
		
		# Make decision
		if state == 1:
			irrigation.pause_irrigation_system()
			# Send alert
			alert(
				user_id=user_id,
				message="Irrigation paused",
				type="INFO"
			)

			return {"message": "Irrigation paused"}

		irrigation.resume_irrigation_system()
		# Send alert
		alert(
			user_id=user_id,
			message="Irrigation resumed",
			type="INFO"
		)

		return {"message": "Irrigation resumed"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
def update_sensors_interval(data: dict) -> dict:
	try:
		# Extract interval
		interval = data['interval']
		user_id = data['user_id']

		# Get job
		scheduler = get_sensors_scheduler()
		if not scheduler:
			# Send alert
			alert(
				user_id=user_id,
				message="No scheduler job found for updates on sensors.",
				type="WARNING"
			)

			return {"error": "Scheduler not initialized"}
		
		# Pause the scheduler for setting the new interval
		scheduler.pause_sensor_updates()

		# Update interval and resume the job
		scheduler.update_interval(interval * 60)

		# Send alert
		alert(
			user_id=user_id,
			message=f"Timer updated to {interval}mins for sensors.",
			type="INFO"
		)

		return {"message": "Sensor updates timer updated."}
		
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

def update_irrigation_interval(data: dict) -> dict:
	try:
		# Extract interval
		interval = data['interval']
		user_id = data['user_id']

		# Get job
		irrigation = get_irrigation_system()
		if not irrigation:
			# Send alert
			alert(
				user_id=user_id,
				message="No irrigation job found.",
				type="WARNING"
			)

			return {"error": "Irrigation not initialized"}
				
		# Stop the scheduler for setting the new interval
		irrigation.pause_irrigation_system()

		# Update interval and resume the job
		irrigation.update_interval(interval * 60)
		
		# Send alert
		alert(
			user_id=user_id,
			message=f"Timer updated to {interval}mins for irrigation.",
			type="INFO"
		)

		return {"message": "Sensor updates timer updated."}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
def update_field_irrigation_config(data: dict) -> dict:
	try:
		# Extract variables
		field_id = data['fieldId']
		user_id = data['userId']

		# Fetch field and user
		field = get_field_by_id(field_id)
		user = get_user_by_id(field_id)

		# Fetch field location
		location = get_location(field['latitude'], field['longitude'])
		# Create config dict
		config = {
			'min_humidity': data['min_humidity'],
			'target_humidity': data['target_humidity'],
			'max_watering_time': data['max_watering_time']
		}

		# Get job
		irrigation = get_irrigation_system()
		if not irrigation:
			return {"error": "Irrigation not initialized"}
		
		# Update config values
		irrigation.update_field_config(field_id, config)

		# Send alert
		alert(
			user_id=user_id,
			message=f"Configuration updated for field on {location[8:]}",
			type="INFO"
		)

		# Send email
		send_email(f"Field: {field['crop_name']} configuration updated at {location[8:]}",
					generate_field_config_update(
						user['email'],
						location[8:],
						config
					),
				user['email'])

		return {"message": f"Field {field_id} config updated."}

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}