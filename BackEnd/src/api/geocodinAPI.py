from dotenv import load_dotenv
import os, requests

from src.services.fields_service import get_field_by_id

# Load .env file
load_dotenv()

def get_location_by_field_id(field_id: str) -> str:

	# Verify field id
	field_data = get_field_by_id(field_id)

	# Return the location
	return (get_location(field_data['latitude'], field_data['longitude']))

def get_location(latitude: float, longitude: float) -> str:
	# Fetch key from .env file
	api_key = os.getenv("GOOGLE_API_KEY")

	if not api_key:
		raise ValueError("API key not found in .env file")
	
	# Google API endpoint
	endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

	# API request params
	params = {
		"latlng": f"{latitude},{longitude}",
		"key": api_key
	}

	# Get response
	response = requests.get(endpoint, params=params)

	# Check status
	if response.status_code == 200:
		# Fetch data
		data = response.json()
		
		if data.get("results"):
			return data["results"][0]["formatted_address"]
		
		else:
			return "No results found."
		
	else:
		return f"Failed to fetch data."
