class Sensor:
    def __init__(self, name, humidity, temperature):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return f"----\nSensor name: {self.name}\nTemperature: {self.temperature:.1f}C\nHumidity: {self.humidity:.2f}%"

    ##########################
    #
    #   Change database JSON to class object
    #
    ###########################
    @classmethod
    def from_dict(obj, data):
        return obj(
            name = data.get('sensor_name'),
            temperature = data.get('temperature'),
            humidity = data.get('humidity')
        )


