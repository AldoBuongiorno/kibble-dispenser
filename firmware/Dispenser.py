from machine import Pin, I2C, PWM, ADC, RTC
from Servo import Servo
from hcsr04 import HCSR04
from Oled import OLED
from led import Led
import time
import utime

MAX_DISTANCE =  31.0
MIN_DISTANCE = 2.0


class Dispenser:
    def __init__(self, pin_led, pin_servo, pin_oled_scl, pin_oled_sda, pin_hcsr04_trigger,
     pin_hcsr04_echo, pin_hcsr04_trigger_1, pin_hcsr04_echo_1, lunch = False, dinner = False, now_date = None): 

        self.led = Led(pin_led) 
        self.servo = Servo(pin_servo)
        self.oled = OLED(128, 64, pin_oled_scl, pin_oled_sda)
        self.hcsr04 = HCSR04(pin_hcsr04_trigger, pin_hcsr04_echo)
        self.hcsr04_1 = HCSR04(pin_hcsr04_trigger_1, pin_hcsr04_echo_1)
        self.__lunch = lunch
        self.__dinner = dinner
        self.now_date = now_date
        self.oled.oled.fill(0)
        

    def open_dispenser(self):
        self.servo.set_angle(90)
        self.led.led_on()
        

    def close_dispenser(self):
        self.servo.set_angle(0)
        self.led.led_off()


    def show_percentage(self):
        self.oled.oled.fill(0)
        distance = self.hcsr04.distance_cm()
        if distance < 0 or distance > MAX_DISTANCE:
            self.oled.show_message('Detection\nError')
            utime.sleep(2)
            return -1.00
        elif 0.0 < distance < MIN_DISTANCE:
            print('MIN_DISTANCE')
            percentage = self.calculate_percentage()
            true_percentage = f"Capacity:{percentage:.0f}%\n"
            self.oled.show_message(true_percentage)
            utime.sleep(2)
            return percentage
        elif 28.0 < distance < MAX_DISTANCE:
            print('MAX_DISTANCE')
            percentage = 0.00
            true_percentage = f"Capacity:{percentage:.0f}%\n"
            self.oled.show_message(true_percentage)
            utime.sleep(2)
            return percentage
        else:
            percentage = self.calculate_percentage()
            true_percentage = f"Capacity:{percentage:.0f}%\n"
            self.oled.show_message(true_percentage)
            utime.sleep(2)
            return percentage


    def dispense_lunch(self):
        
        distance = self.hcsr04_1.distance_cm()
        lunch_inf = 12
        lunch_sup = 14
        if distance < 100 and self.show_percentage() != -1.0 and self.show_percentage() != 0.0 :
            if lunch_inf <= self.now_date <= lunch_sup and self.__lunch is False:
                self.__auto_feed()
                self.__lunch = True               
                self.__dinner = False
                return self.__lunch 
    

    def dispense_dinner(self):
        
        distance = self.hcsr04_1.distance_cm()
        dinner_inf = 19
        dinner_sup = 22
        
        if distance < 100 and self.show_percentage() != -1.0 and self.show_percentage() != 0.0 :
            if dinner_inf <= self.now_date <= dinner_sup and self.__dinner is False:
                self.__auto_feed()
                self.__dinner = True
                self.__lunch = False
                return self.__dinner

    
    def check_meal(self, hour):
        
        self.now_date = hour
        if(self.now_date == 0):
            self.__lunch = False
            self.__dinner = False
    
    
    def calculate_percentage(self):
        
        distance = self.hcsr04.distance_cm()
        percentage = (distance*100)/MAX_DISTANCE
        return (100-percentage)
        
    def manual_feed(self):
        self.open_dispenser()
        self.oled.show_message('Dispensing\nKibbles')
        time.sleep(5)
        self.close_dispenser()
    
    def __auto_feed(self):
        self.open_dispenser()
        time.sleep(5)
        self.close_dispenser()        
        
