import RPi.GPIO as GPIO
import time

from buttons import *

button1 = Button(10)
button2 = Button(15)


print("Waiting for button press (CTRL+C to exit)...")
try:
    #EVENT LOOP
    while True:
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
