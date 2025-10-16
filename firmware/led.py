from machine import Pin
from time import sleep

class Led:

    def __init__(self, pin):
        self.led=Pin(pin, Pin.OUT)

    def led_on(self):
        self.led.on()

    def led_off(self):
        self.led.off()    



