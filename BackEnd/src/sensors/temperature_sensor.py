import os
import glob
import time
import logging 

#######################
#
#   Define sensors path and load
#   correct modules
#
#######################
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

DIR = '/sys/bus/w1/devices/'

#
#   Retrieve sensor file
#
def sensor_file(port):
	logging.debug('\t ===> Inside temperature file')
	# Open folder for specific sensor
	folder = glob.glob(DIR + '28*')[port]
	logging.debug(f'Folder: {folder}')

	# Return slave file 
	return folder + '/w1_slave'

#
#   Fetch file data lines
#
def read_temperature(slave_file):
	# Open file on read mode
	file = open(slave_file, 'r')
	# Fetch file lines
	lines = file.readlines()
	
	'''
		Slave file contains two lines of data.
	At the end of the first line is a 'trigger' of value
	YES or NO that tells us if temperature is measured or not

	Ending of the second line provides us the raw temperature data
	as : t=xxxx. 
	'''
	while lines[0].strip()[-3:] != 'YES':
		continue

	temp_pos = lines[1].find("t=")
	if temp_pos != -1:
		temp_data = lines[1][temp_pos+2:]
		temp_celsius  = float(temp_data) / 1000.0

		# Close file
		file.close()

		logging.info(f"Retrieve temperature: {temp_celsius:.2f}")
		return temp_celsius
	
	# Close file
	file.close()
