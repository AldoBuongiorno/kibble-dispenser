from machine import Pin, I2C, PWM, ADC, RTC
from Servo import Servo
from hcsr04 import HCSR04
from Oled import OLED
from led import Led
from Dispenser import Dispenser
from time import time
import utime

class Datetime:
    def __init__(self):
        self.hour = None
        
    def setHour(self, hour):
        if hour is not None:
            # Converte la stringa in un intero
            self.hour = int(hour.decode('utf-8'))
            
    def getHour(self):
        return self.hour
    

        
     
        