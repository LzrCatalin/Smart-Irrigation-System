import logging

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler

from src.classes.SensorScheduler import SensorScheduler
from src.sensors.humidity_sensor import *

from src.controllers.sensors_controller import *
from src.controllers.users_controller import *
from src.controllers.fields_controller import *
from src.controllers.oauth_controller import *

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

####################
#
#   Logging config
#
####################
logging.basicConfig(
	level = logging.DEBUG,
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

# Start periodic update at a 30 seconds interval
# sensors_scheduler.schedule_sensor_updates(5)

####################
#
#   Blueprints Initializations
#
####################
# sensors_init()
# app.register_blueprint(sensors_bp)
app.register_blueprint(users_bp)
app.register_blueprint(fields_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
	app.run(debug=False, host = "0.0.0.0", port = 8080)
	