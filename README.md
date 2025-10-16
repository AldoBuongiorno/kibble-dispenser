# Kibble Dispenser 

An IoT-based **automatic kibble dispenser** built with **ESP32 (MicroPython)** and a **Node-RED dashboard**.  
The system allows local and remote control of the dispenser through MQTT communication, providing live monitoring of food level, manual dispensing, and notifications when the container is almost empty.

---

## 📦 Project Overview

This project combines embedded firmware and a cloud-connected dashboard to create a smart feeding system for pets.  

- The **ESP32** handles all hardware-related operations:
  - Motor control for dispensing kibble
  - Weight or distance sensor reading for remaining capacity
  - OLED screen updates
  - MQTT communication with the dashboard
- The **Node-RED** dashboard displays real-time data, provides manual control buttons, and logs feeding events.

The system communicates via the **public MQTT broker** at `test.mosquitto.org`, using a dedicated namespace of topics.

---

## 🧠 Architecture
ESP32 (MicroPython) --> MQTT Broker --> Node-RED Dashboard

---

## ⚙️ Technologies Used

**Hardware:**  
- ESP32 microcontroller  
- Motor + feed mechanism  
- Ultrasonic or weight sensor  
- OLED display (I²C)

**Software:**  
- MicroPython  
- Node-RED + Node-RED Dashboard  
- MQTT (public broker: test.mosquitto.org)  
- JSON messaging for data exchange  

---

## 🚀 Getting Started

### 1️⃣ ESP32 Firmware Setup
1. Flash **MicroPython** onto the ESP32.  
2. Copy all files from the `/firmware` directory to the board (via **Thonny** or **ampy**).  
3. Configure Wi-Fi and MQTT settings inside `main.py` or `config.py` (if provided).  
4. Run the script — the OLED display should show startup messages.  

The ESP32 will:
- Measure dispenser capacity (`calculate_percentage()`)
- Handle manual and automatic feeding routines
- Publish MQTT messages

---

### 2️⃣ Node-RED Dashboard Setup
1. Import the flow from `/node-red/flows.json` into your Node-RED editor.  
2. Open the **MQTT configuration node** and verify:
 - Broker: `test.mosquitto.org`
 - Port: `1883`
 - Topics: match the ones listed above
3. Deploy the flow.  
4. Access the dashboard at: http://<your-node-red-host>:1880/ui

You will find:
- **Capacity gauge** (remaining food)
- **Manual Feed** and **Reset** buttons
- **Charts** of feeding events
- **Notifications** for “almost empty” or “empty” status  

---

## 📊 Features

✅ Real-time monitoring of dispenser capacity  
✅ Manual and automatic feeding logic  
✅ OLED feedback on device status  
✅ MQTT-based communication between device and dashboard  
✅ Node-RED dashboard with charts and logs  
✅ Notifications for “almost empty” conditions  

---

## 🧩 Future Improvements

- Replace the public MQTT broker with a **local/private instance** (e.g., Mosquitto on Raspberry Pi)  
- Add **authentication** for MQTT and dashboard access  
- Schedule feeding times from Node-RED

---

## 🪪 License
This project is released **without a license**.  
All rights reserved unless explicitly stated otherwise.  
If you intend to reuse or modify the code, please contact the author.

---

## 👨‍💻 Author
Developed by **Aldo Buongiorno, Ciro Cutolo, Salvatore Francesco Tartaglione, Raffaele Calabrese**. 
