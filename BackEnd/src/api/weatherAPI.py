import os
import time
import requests
from dotenv import load_dotenv

# load .env file
load_dotenv()

#######################
#
#   API Setup
#
#######################
api_key = os.getenv('WEATHER_API')

######################
#
#   Retrieve URL informations in JSON format
#
#######################

def retrieve_weather_data(city):
	url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
	try:
		response = requests.get(url, timeout=5)
		if response.status_code == 200:
			data = response.json()
			return {
				'temp': data['current']['temp_c'],
				'humidity': data['current']['humidity'],
				'condition': data['current']['condition']['text'],
				'precip_mm': data['current']['precip_mm'],
				'wind_kph': data['current']['wind_kph']
			}
		else:
			print(f"Weather API error: {response.status_code}")
			return None
	except Exception as e:
		print(f"Error while calling weather API: {e}")
		return None

if __name__ == "__main__":

	print(retrieve_weather_data("Timisoara"))