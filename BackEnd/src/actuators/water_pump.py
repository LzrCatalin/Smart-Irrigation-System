import time, logging
import RPi.GPIO as GPIO

###################
#
#	Pump setup
#
###################
pump_pin = 27

def pump_setup() -> None:
	logging.debug('Initializing water pump setup.')
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pump_pin, GPIO.OUT)
	GPIO.output(pump_pin, GPIO.HIGH)
	logging.debug('Initialization finished.')

###################
#
#	Start Pump
#
###################
def pump_start() -> None:
	pump_setup()
	GPIO.output(pump_pin, GPIO.LOW)
	logging.debug('Pump working...')

###################
#
#	Stop Pump
#
###################
def pump_stop() -> None:
	GPIO.output(pump_pin, GPIO.HIGH)
	logging.debug('Pump done.')
	GPIO.cleanup()
	logging.debug('GPIO clean.')

###################
#
#	Start Pump for a time period
#
###################
def irrigation_cycle(duration: int) -> None:
	logging.debug(f'Pump working for {duration} seconds.')
	pump_setup()
	pump_start()
	time.sleep(duration)
	pump_stop()