import os, atexit, logging
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from src.classes.SensorScheduler import SensorScheduler
from src.sensors.humidity_sensor import *
from src.controllers.sensors_controller import *
from src.services.sensors_services import *
####################
#
#   Add the path to the project
#
####################
import sys
sys.path.append("src")

app = Flask(__name__)

####################
#
#   Logging config
#
####################
logging.basicConfig(
	level = logging.INFO,
	format =  '%(levelname)s - %(message)s',
	handlers = [logging.StreamHandler()]
)

####################
#
#   Scheduler configurations
#
####################
class Config:
	SCHEDULER_API_ENABLE = True

app.config.from_object(Config())

# Init sensor scheduler
# sensors_scheduler = SensorScheduler(app)

# # Start periodic update at a 30 seconds interval
# sensors_scheduler.schedule_sensor_updates(10)

####################
#
#   Blueprints Initializations
#
####################
# start_sensors_measurement()
app.register_blueprint(sensors_bp)

if __name__ == '__main__':
	app.run(debug=False, host = "0.0.0.0", port = 8080)
	