import time
import ubinascii
import machine
import micropython
import network
import esp
import gc
from umqtt.simple import MQTTClient

esp.osdebug(None)
gc.collect()

ssid = "YOUR_WIFI_SSID"
password = 'YOUR_WIFI_PASSWORD'

def connect_to_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to Network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('Network config:', sta_if.ifconfig())

connect_to_wifi(ssid, password)

import main