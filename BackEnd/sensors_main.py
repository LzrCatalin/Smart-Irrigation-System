import os, logging

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS

from src.classes.SensorScheduler import SensorScheduler
from src.classes.FieldIrrigationSystem import FieldIrrigationSystem
from src.actuators.water_pump import  *
from src.sensors.humidity_sensor import *

from src.controllers.sensors_controller import sensors_bp
from src.controllers.actuators_controller import actuators_bp
from src.services.sensors_services import *
from src.firebase.sensors_init import sensors_init

####################
#
#   Add the path to the project
#
####################
import sys
sys.path.append("src")

app = Flask(__name__)

app.secret_key = os.urandom(24)

CORS(app)

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

# Create irrigation system
irrigation_system = FieldIrrigationSystem(app)

# Init sensor scheduler
sensors_scheduler = SensorScheduler(app, irrigation_system)

# Set the scheduler into irrigation system
irrigation_system.set_scheduler(sensors_scheduler)

# Schedule cycles
sensors_scheduler.schedule_sensor_updates(45)
irrigation_system.schedule_irrigation_cycles(60)

####################
#
#   Blueprints Initializations
#
####################
app.register_blueprint(sensors_bp)
app.register_blueprint(actuators_bp)


if __name__ == '__main__':
	app.run(debug=False, host = "0.0.0.0", port = 5000)
