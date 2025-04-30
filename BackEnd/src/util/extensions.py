from flask import current_app

def get_sensors_scheduler():
    return current_app.config.get('SENSORS_SCHEDULER')

def get_irrigation_system():
    return current_app.config.get('IRRIGATION_SYSTEM')