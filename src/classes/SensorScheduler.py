import atexit
from colorama import Fore
from flask_apscheduler import APScheduler
from src.firebase.services import sensors_services
from src.classes.Sensor import Sensor
from src.sensors.testFunctions import *
from src.sensors.humidity_sensor import *
####################
#
#   Scheduler configurations
#
####################
class SensorScheduler:
    def __init__(self, app):
        self.scheduler = APScheduler()
        self.scheduler.init_app(app)
        self.scheduler.start()
    
    def periodic_sensor_update(self):
            # Fetch all ids from Firebase
            sensor_ids = sensors_services.get_sensors_ids()

            # Iterate through sensors ids
            for id in sensor_ids:
                # Retrieve sensor data based on id
                sensor_data = sensors_services.get_sensor_data(id)
                
                # Fetch sensor port
                port = sensor_data['port']
                
                # Fetch adc_value based on port
                if port is not None:
                    adc_value = sensor_setup(port)

                if sensor_data:
                    # Create Sensor obj with update data
                    sensor = Sensor(
                        id = sensor_data['id'],
                        name = sensor_data['sensor_name'],
                        temperature = calculate_temperature_percentage(),
                        humidity = calculate_moisture_percentage(adc_value),
                        port = sensor_data['port']
                    )
                    
                    # Insert new data into Firebase
                    sensors_services.update_sensor_by_id(id, sensor)

    def schedule_sensor_updates(self, duration):
        print(f"Sensor scheduler Turn ON for every {duration} seconds.")
        self.scheduler.add_job(id='sensor_update', 
                        func=self.periodic_sensor_update,
                        trigger = 'interval', 
                        seconds = duration)
        
    def scheduler_shutdown(self):
        print("Sensors scheduler shutdown.")
        atexit.register(lambda: self.scheduler_shutdown())

    def get_schedules(self):
        print(self.scheduler.get_jobs())


