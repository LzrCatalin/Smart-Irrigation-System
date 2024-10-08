class Sensor:
    def __init__(self, name, humidity, temperature):
        self.name = name
        self.humidity = humidity
        self.temperature = temperature

    def __str__(self):
        return f"----\nSensor name: {self.name}\nHumidity: {self.humidity:.2f}%\nTemperature: {self.temperature:.1f}C"



