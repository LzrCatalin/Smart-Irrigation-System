import logging

from src.util.utils import alert
from src.util.mail_sender import send_email, generate_field_config_update
from src.util.extensions import get_irrigation_system, get_sensors_scheduler
from src.services.fields_service import get_field_user, get_field_by_id, get_location
from src.services.users_service import get_user_by_id

def push_into_system(field_id: str) -> dict:
	try:
		# Get the working system
		system = get_irrigation_system()

		# Get field's user
		user_id = get_field_user(field_id)
		field_data = get_field_by_id(field_id)

		if system:
			# Push the field id into the system
			system.add_field(field_id)

			# Send alert
			alert(
				user_id=user_id,
				message=f"Crop {field_data['crop_name']} added into the system.",
				type="INFO"
			)

			return {"message": "OK"}
		
		return {"error": "Job not found."}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

def remove_from_system(field_id: str) -> dict:
	try:
		# Get the working system
		system = get_irrigation_system()
		
		# Get field's user
		user_id = get_field_user(field_id)
		field_data = get_field_by_id(field_id)

		if system:
			# Remove data from system
			system.remove_field(field_id)

			# Send alert
			alert(
				user_id=user_id,
				message=f"{field_data['crop_name']} removed from the system.",
				type="INFO"
			)

			return {"message": "OK"}
		
		return {"error": "Job not found."}
	
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
			'max_watering_time': data['max_watering_time'] * 60
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
			message=f"[{field['crop_name']}] system configuration updated.",
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