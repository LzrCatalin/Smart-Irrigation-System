from flask import Flask, jsonify, request
from src.controllers.sensors_controller import create_sensors_controller
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
#   Register controllers
#
####################
create_sensors_controller(app)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 8080)
    