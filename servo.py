import RPi.GPIO as GPIO
import time
import threading
from util import *

class ServoPin(Pin):
    def __init__(self, gpio_pin):
        super().__init__(gpio_pin)

        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.LOW)

class ServoMotor:
    STEP_COUNT = 4096 # One rotation
    STEP_SLEEP = 0.0006 # Fastest possible (For me)
    STEP_SEQUENCE = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]

    def __init__(self, pins: list[Pin] = None):
        self.pins: list[ServoPin] = pins
        self.lock: threading.Lock = threading.Lock()

    def addPin(self, pin: ServoPin):
        self.pins.append(pin)

    def cleanup(self):
        with self.lock:
            for pin in self.pins:
                pin.cleanup()

    def run(self, move):
        motorStepCounter = 0
        pinsCount = len(self.pins)

        for pin in self.pins:
            pin.__init__(pin.gpio_pin)
        for _ in range(self.STEP_COUNT):
            for pin in range(0, pinsCount):
                GPIO.output(self.pins[pin].gpio_pin, self.STEP_SEQUENCE[motorStepCounter][pin] )
            motorStepCounter = move(motorStepCounter)
            time.sleep(self.STEP_SLEEP)
        
        self.lock.release()

    def run_in_thread(func):
        def wrapper(self, *args, **kwargs):
            if not self.lock.acquire(blocking=False):
                return
            thread = threading.Thread(target=func, args=(self, *args), kwargs=kwargs)
            thread.start()
        return wrapper
    
    def right(self, counter):
        return (counter - 1) % 8

    def left(self, counter):
        return (counter + 1) % 8

    @run_in_thread
    def turnRight(self):
        self.run(self.right)

    @run_in_thread
    def turnLeft(self):
        self.run(self.left)

    @staticmethod
    def predefinedServo():
        in1 = ServoPin(13)
        in2 = ServoPin(6)
        in3 = ServoPin(19)
        in4 = ServoPin(26)

        return ServoMotor([in1, in2, in3, in4])

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    motor = ServoMotor.predefinedServo()

    try:
        motor.turnRight()
        while True:
            motor.turnLeft()
            time.sleep(0.1)

        exitCode = 0
    except KeyboardInterrupt:
        exitCode = 1
    except Exception as e:
        print(e)
        exitCode = 1
    
    motor.cleanup()
    exit(exitCode)