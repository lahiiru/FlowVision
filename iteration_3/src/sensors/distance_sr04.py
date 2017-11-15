from distance_sensor import DistanceSensor
import RPi.GPIO as GPIO
import time


class DistanceSR04(DistanceSensor):
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def get_real_time_distance_cm(self):
        # set Trigger to HIGH
        GPIO.output(self.trig_pin, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance
