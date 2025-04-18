import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        return GPIO.input(self.gpio_pin) == GPIO.LOW


if __name__ == "__main__":
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
