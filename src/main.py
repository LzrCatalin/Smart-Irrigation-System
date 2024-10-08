from classes.Sensor import Sensor
from firebase.services import sensors_services

if __name__ == '__main__':
    sensor1 = Sensor("sensor1", 25.12, 29.1)
    sensor2 = Sensor("sensor2", 26.2, 25.0)

    sensors_data = [sensor1, sensor2]

    # Add sensors data to db
    # for data in sensors_data:
    #     sensors_services.add_sensor_data(data)

    # Display data for sensor id
    sensors_services.get_sensor_data(10)

    