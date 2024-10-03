import time
import requests

#######################
#
#   API Setup
#
#######################
api_key = "api_key"
city = "Timisoara"
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

######################
#
#   Retrieve URL informations in JSON format
#
#######################
response = requests.get(url)
data = response.json()
print(data) # Print JSON

def retrieve_weather_data():
    if response.status_code == 200: # Request successfully
        localtime = data['location']['localtime'].split() # Parse localtime to retrieve date and hour
        localtime_date = localtime[0]
        localtime_hour = localtime[1]
        temp_c = data['current']['temp_c']
        humidity = data['current']['humidity']
        condition = data['current']['condition']['text'] # Retrieve only text from condition JSON

        # Print data
        print(f"City: {city}")
        print(f"Date: {localtime_date}\nHour: {localtime_hour}")
        print(f"Temperature: {temp_c}")
        print(f"Humidity: {humidity}")
        print(f"Condition: {condition}")

    else:
        print("Failed to retrieve data...")

try:
    retrieve_weather_data()

except KeyboardInterrupt:
    print("Existing...")
