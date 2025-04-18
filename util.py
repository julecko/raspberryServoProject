import RPi.GPIO as GPIO

class Pin():
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin

    def cleanup(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)