import RPi.GPIO as GPIO
import time
from buttons import *
from servo import *

GPIO.setmode(GPIO.BCM)

buttonRight = Button(10)
buttonLeft = Button(15)
motor = ServoMotor.predefinedServo()

turning_left = False
turning_right = False
print("Waiting for button press (CTRL+C to exit)...")
try:
    #EVENT LOOP
    while True:
        time.sleep(0.01)
        if buttonRight.is_pressed():
            print("Turn right")
            if turning_left:
                turning_left = False
                continue
            turning_right = True
        
        if turning_right:
            motor.turnRight()
        
        if buttonLeft.is_pressed():
            print("Turn left")
            if turning_right:
                turning_right = False
                continue
            turning_left = True
        
        if turning_left:
            motor.turnLeft()
except KeyboardInterrupt:
    print("Exiting...")
    motor.cleanup()
    GPIO.cleanup()
