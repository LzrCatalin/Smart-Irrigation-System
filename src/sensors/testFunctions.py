import random

"""
    Create two function to simulate
	sensor fetched data in real life
	for humidity and temperature with only 2 digits
"""

def calculate_moisture_percentage():
	percentage = round(random.uniform(0.00, 100.00), 2)
	return percentage

def calculate_temperature_percentage():
	percentage = round(random.uniform(0.00, 100.00), 2)
	return percentage
	