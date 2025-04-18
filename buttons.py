import RPi.GPIO as GPIO
import time
from util import *

class Button(Pin):
    def __init__(self, gpio_pin):
        super().__init__(gpio_pin)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.last_pressed_time = None
        self.timeout = 0

    def set_timeout(self, timeout_seconds):
        self.timeout = timeout_seconds

    def is_pressed(self):
        if GPIO.input(self.gpio_pin) == GPIO.LOW:
            if self.last_pressed_time is None:
                self.last_pressed_time = time.time()
            elif time.time() - self.last_pressed_time > self.timeout:
                return False
            return True
        else:
            self.last_pressed_time = None
            return False


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    button_pin1 = Button(10)
    button_pin2 = Button(15)

    print("Waiting for button press (CTRL+C to exit)...")

    try:
        while True:
            if button_pin1.is_pressed():
                print("Button pressed hello!")
            else:
                print("Button not pressed")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()
