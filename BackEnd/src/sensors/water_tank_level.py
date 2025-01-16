import time
import RPi.GPIO as GPIO

#######################
#
#	Setup
#
########################
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Define jar's height
JAR_HEIGTH_CM = 14 # Approximativly the height of the sensor
MAX_WATER_HEIGHT_CM = 10 # Maximum height of water in jar

#######################
#
#	Function to retrieve measured distance
#
########################
def measure_distance():
    print("Process starts")
    # Start send pulse
    GPIO.output(TRIG, False) # Send the pulse
    print("Sending pulse...")
    time.sleep(0.0001)
    GPIO.output(TRIG, True) # Stop sending
    print("Stop sending pulse")
    
    # Wait for signal
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        
    # Receiving the signal from the trigger
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
                
    pulse_duration = pulse_end - pulse_start
    
    # Get the distance. Multiply with 34300 because is the aprox. speed of sound in cm/s
    distance = (pulse_duration * 34300) / 2
    
    #print(f"\nMeasured distance: {distance} cm\n")
    return distance

#######################
#
#	Function to determine water level
#
########################
def get_water_level():
    #print("Start measuring distance...")
    distance = measure_distance()
    
    # Verify distance
    if distance > JAR_HEIGTH_CM:
        print("No water detected")
        return 0
    
    # Get the water level
    water_level = JAR_HEIGTH_CM - distance
    water_percentage = (water_level / MAX_WATER_HEIGHT_CM) * 100
    
    #print(f"Water level: {water_level:.2f} cm\n")
    print(f"Water percentage: {water_percentage:.1f}%\n")

#######################
#
#	Start Measurements
#
#######################
def start():
    get_water_level()

#######################
#
#	Stop Measurements
#
#######################
def stop():
    GPIO.cleanup()
    print("Successfully stopped water measurements")
    
    
#try:
#   while True:
#        start()
#        time.sleep(5)
        
#except KeyboardInterrupt:
#    GPIO.cleanup()