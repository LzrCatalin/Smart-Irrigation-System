import logging

from src.actuators.water_pump import pump_start, pump_stop
from src.util.extensions import get_sensors_scheduler, get_irrigation_system

####################
#
#	Util functions
#
####################
def toggle_water_pump(data: dict) -> dict:
	try:
		# Extract state
		state = data['state']

		if state == 1:
			pump_start()
			return {"message": "WATER PUMP -> ON"}
		
		pump_stop()
		return {"message": "WATER PUMP -> OFF"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

def toggle_scheduler_activity(data: dict) -> dict:
	try:
		# Extract state
		state = data['state']
		
		# Get job
		scheduler = get_sensors_scheduler()
		if not scheduler:
			return {"error": "Scheduler not initialized"}

		# Make decision
		if state == 1:
			scheduler.pause_sensor_updates()
			return {"message": "Scheduler paused"}

		scheduler.resume_sensor_updates()
		return {"message": "Scheduler resumed"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
def toggle_irrigation_activity(data: dict) -> dict:
	try:
		# Extract state
		state = data['state']

		# Get job
		irrigation = get_irrigation_system()
		if not irrigation:
			return {"error": "Irrigation not initialized"}
		
		# Make decision
		if state == 1:
			irrigation.pause_irrigation_system()
			return {"message": "Irrigation paused"}

		irrigation.resume_irrigation_system()
		return {"message": "Irrigation resumed"}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
def update_sensors_interval(data: dict) -> dict:
	try:
		# Extract interval
		interval = data['interval']

		# Get job
		scheduler = get_sensors_scheduler()
		if not scheduler:
			return {"error": "Scheduler not initialized"}
		
		# Pause the scheduler for setting the new interval
		scheduler.pause_sensor_updates()

		# Update interval and resume the job
		scheduler.update_interval(interval * 60)
		return {"message": "Sensor updates timer updated."}
		
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}

def update_irrigation_interval(data: dict) -> dict:
	try:
		# Extract interval
		interval = data['interval']

		# Get job
		irrigation = get_irrigation_system()
		if not irrigation:
			return {"error": "Irrigation not initialized"}
				
		# Stop the scheduler for setting the new interval
		irrigation.pause_irrigation_system()

		# Update interval and resume the job
		irrigation.update_interval(interval * 60)
		return {"message": "Sensor updates timer updated."}
	
	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}
	
def update_field_irrigation_config(data: dict) -> dict:
	try:
		# Extract variables
		field_id = data['fieldId']

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

		return {"message": f"Field {field_id} config updated."}

	except KeyError as e:
		return {"error": f"Key missing: {str(e)}"}