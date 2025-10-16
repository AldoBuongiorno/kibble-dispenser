import machine, time
from machine import Pin, I2C
import ssd1306
import utime

MAX_DISTANCE = 30

class OLED:
    """
    Driver to use the display which shows infos about dispenser fullness
    """
    def __init__(self, width, height, scl_pin, sda_pin):
        """
        width: oled width 
        height: oled height
        scl_pin: 
        sda_pin:   
        """
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.oled_width = width
        self.oled_height = height
        self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, i2c)	
        self.error = "Errore nella rilevazione"  

    
    def show_message(self, text):
        self.oled.fill(0)
        array = text.split("\n")
        split =  [s.strip() for s in array]
        height = 15
        if(len(split) == 2 and split[1] == '') :
            self.oled.text(split[0], 20, 30)
        else :
            for i in range(len(split)) :
                self.oled.text(split[i], 20, height)
                height += 16
        self.oled.show()
        utime.sleep(1)
                    
            
    


