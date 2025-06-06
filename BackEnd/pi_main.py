import os, logging

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS

from src.classes.SensorScheduler import SensorScheduler
from src.classes.FieldIrrigationSystem import FieldIrrigationSystem
from src.controllers.sensors_controller import sensors_bp
from src.controllers.actuators_controller import actuators_bp
from src.controllers.irrigation_config_controller import system_bp

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
sensors_scheduler.schedule_sensor_updates(20)		# 15 Mins Default
irrigation_system.schedule_irrigation_cycles(60)	# 2H Default

app.config['SENSORS_SCHEDULER'] = sensors_scheduler
app.config['IRRIGATION_SYSTEM'] = irrigation_system
####################
#
#   Blueprints Initializations
#
####################
app.register_blueprint(sensors_bp)
app.register_blueprint(actuators_bp)
app.register_blueprint(system_bp)

if __name__ == '__main__':
	app.run(debug=False, host = "0.0.0.0", port = 5000)
