import time
import RPi.GPIO as GPIO

###################
#
#	Pump setup
#
###################
pump_pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
#print("Setup Completed")

###################
#
#	Start Pump
#
###################
def start():
    GPIO.output(pump_pin, GPIO.LOW)
    print("Pump ON")

###################
#
#	Stop Pump
#
###################
def stop():
    GPIO.output(pump_pin, GPIO.HIGH)
    print("Pump OFF")
  
###################
#
#	Start Pump for a time period
#
###################
def working_pump(time):
    print("Pumping water for: {time} seconds")
    start()
    time.sleep(time)
    stop()
    
#try:
#    pump_water()
    
#except KeyboardInterrupt:
#    GPIO.cleanup()

#finally:
#    GPIO.cleanup()