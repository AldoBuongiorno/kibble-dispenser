from machine import Pin, I2C, PWM, ADC
from Dispenser import Dispenser
from datetime import Datetime
import utime
import time
import ujson
from umqtt.simple import MQTTClient
import ubinascii
import machine



client_id = ubinascii.hexlify(machine.unique_id())
mqtt_server = 'test.mosquitto.org'
mqtt_user = ''
mqtt_pass = ''

#topic
topic_sub = b'unisa/IoT/gruppo07/giveTreat'
topic_sub1 = b'unisa/IoT/gruppo07/reset'
topic_sub2 = b'unisa/IoT/gruppo07/takeTime'
topic_pub = b'unisa/IoT/gruppo07/pienezza_dispenser'
topic_pub1 = b'unisa/IoT/gruppo07/giveTreatAutoLaunch'
topic_pub2 = b'unisa/IoT/gruppo07/giveTreatAutoDinner'
topic_pub3 = b'unisa/IoT/gruppo07/treatGiven'
topic_pub4 = b'unisa/IoT/gruppo07/almostEmpty'
topic_pub5 = b'unisa/IoT/gruppo07/acquireTime'

#variabili 
last_message = 0
message_interval = 1
last_send = 0
interval = 25   #invia notifica problemi di capacità ogni 30 secondi
flag = True
date_time = Datetime()
dispenser = Dispenser(2, 12, 25, 26, 14, 27, 33, 32)

#inizializzazione
dispenser.oled.show_message('Starting :)\n')

def build_message(msg):
    """
    Costruisce il messaggio da inviare al brocker MQTT

    Ritorna 
    -------
    JSON
        Il messaggio da inviare al brocker MQTT in caso di intero
    
    Stringa
        Il messaggio da inviare al brocker MQTT in caso di stringa
    """
    if type(msg) == int:
        return ujson.dumps({
                "percentage" : msg,
                "notificationAlmostEmpty": "Dispenser quasi vuoto",
                "notificationEmpty": "Dispenser vuoto",
                "notificationError": "Errore nella rilevazione"
            })
    else: #type(msg) == str:
        return msg


def sub_cb(topic, msg):      
    """
    Funzione di callback per la ricezione dei messaggi in base ai topic sottoscritti
    
    1. unisa/IoT/gruppo07/giveTreat -> Erogazione manuale dei croccantini
    2. unisa/IoT/gruppo07/reset -> Reset del dispositivo
    3. unisa/IoT/gruppo07/takeTime -> Acquisizione dell'ora corrente e controllo dell'erogazione dei pasti


    """       
    if topic == b'unisa/IoT/gruppo07/giveTreat':
        dispenser.manual_feed()
        msg = build_message('Croccantini Erogati')
        client.publish(topic_pub3, msg)
    elif topic == b'unisa/IoT/gruppo07/reset':
        dispenser.oled.show_message('Resetting...\n')
        machine.reset()
    elif topic == b'unisa/IoT/gruppo07/takeTime':
        date_time.setHour(msg)
        hour = date_time.getHour()
        if hour == 00 or hour != dispenser.now_date :
            dispenser.check_meal(hour)
        

def connect_and_subscribe():
    """
    Connessione al brocker MQTT e sottoscrizione ai topic

    Ritorna
    -------
    Oggetto MQTTClient 
        Il client connesso al brocker MQTT
    """
    client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    client.subscribe(topic_sub1)
    client.subscribe(topic_sub2)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))     
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub1))    
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub2))    
    return client

def restart_and_reconnect():
    """
    Funzione di riconnessione al brocker MQTT
    """
    print('Failed to connect to MQTT broker. Reconnecting...')
    dispenser.oled.show_message('Connection\nFailed:\nReconnecting')
    time.sleep(10)
    machine.reset()     

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()
  


while True:
    try:
        client.check_msg()
        
        if (time.time() - last_message) > message_interval:
            print('message interval')
            msg = dispenser.calculate_percentage()
            msg1 = build_message(msg)
            client.publish(topic_pub, msg1)
            message = build_message("Acquisici")
            client.publish(topic_pub5, message)
            dispenser.show_percentage(msg)
            
            if (time.time() - last_send) > interval or flag == True:
                print('intervallo')
                flag = True
                msg = dispenser.calculate_percentage()
                msg1 = build_message(msg)
                client.publish(topic_pub, msg1)  
                client.publish(topic_pub4, msg1) 
                if msg <= 20.0 and msg != -1.0 and msg != 0.0:
                    dispenser.oled.show_message('Dispenser\nAlmost\nEmpty')
                    utime.sleep(2)
                    flag = False
                if msg == 0.0: 
                    flag = False
                last_send = time.time()

            dispenser.show_percentage(msg)

            if(date_time.getHour() != None):
                if dispenser.dispense_lunch(msg):     
                    msg0 = build_message('Pranzo Erogato')
                    client.publish(topic_pub1, msg0)
                    dispenser.oled.show_message('Lunch Ready\n')
                elif dispenser.dispense_dinner(msg):
                    msg0 = build_message('Cena Erogata')
                    client.publish(topic_pub2, msg0)
                    dispenser.oled.show_message('Dinner Ready\n')
            
            last_message = time.time()
            
    except OSError as e:
        restart_and_reconnect()
        






