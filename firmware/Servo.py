from machine import Pin, PWM
import time
import math

class Servo:
    def __init__(self, pin, freq=50, min_duty=26, max_duty=123, angle=0):
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.impulse = 0
        self.freq = freq
        self.angle = angle
        self.servo = PWM(Pin(pin), freq, duty=0)
        self.set_angle(self.angle)
    
    def set_angle(self, angle):
        """Sets the angle to 'angle' degrees, by altering the duty"""
        duty_min = 26
        duty_max = 123
        duty = int(duty_min + (angle/180)*(duty_max-duty_min))
        self.servo.duty(duty)



