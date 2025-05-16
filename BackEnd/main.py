import logging, os

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS

from src.classes.OAuthManager import OAuthManager

from src.controllers.sensors_controller import sensors_bp
from src.controllers.users_controller import users_bp
from src.controllers.fields_controller import fields_bp
from src.controllers.oauth_controller import auth_bp
from src.controllers.alerts_controller import alerts_bp
from src.controllers.history_controller import irrigations_bp

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

# OAuth Manager Setup
oauth_manager = OAuthManager(app)
app.oauth_manager = oauth_manager

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

####################
#
#   Blueprints Initializations
#
####################
# sensors_init()
app.register_blueprint(sensors_bp)
app.register_blueprint(users_bp)
app.register_blueprint(fields_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(irrigations_bp)

if __name__ == '__main__':
	app.run(debug=False, host = "0.0.0.0", port = 5000)
	