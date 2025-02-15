# BMH Water Management System

## Overview
The BMH Water Management System is a solution designed to monitor and manage the water levels in multiple tanks using ultrasonic sensors, display data on an LCD screen, and send SMS alerts to designated phone numbers when the water levels reach predefined thresholds. The system also provides scheduled SMS notifications for water system status and allows users to request the current water status via SMS.

## Features
- **Water Tank Monitoring**: Uses ultrasonic sensors to measure water levels in four different tanks.
- **SMS Notifications**: Sends SMS alerts when water levels fall below certain thresholds (75%, 50%, 25%).
- **Scheduled Alerts**: Sends daily SMS updates with water tank volumes and percentages at 7:00 AM and 6:30 PM.
- **SMS Status Request**: Allows users to request the current water system status via SMS.
- **Real-time Display**: Displays water levels and volumes on a 20x4 LCD screen.
- **Multiple Contact Numbers**: Sends alerts to multiple phone numbers.

## Components
- **Hardware**:
  - GSM Module (SIM900 or similar) for sending SMS.
  - 4 Ultrasonic Sensors (HC-SR04) for measuring water levels.
  - LCD Display (20x4) for displaying water levels and tank status.
  - Real-Time Clock (RTC DS3231) for accurate time-based operations.
- **Software**:
  - Arduino IDE for writing and uploading code to the Arduino.
  - Libraries: `SoftwareSerial`, `LiquidCrystal`, `Wire`, `RTClib`.

## System Setup

### GSM Setup
The GSM module is connected via SoftwareSerial on pins 10 (RX) and 11 (TX). Ensure that your GSM module is properly connected and has a SIM card with SMS capability.

### LCD Setup
The LCD is connected to pins 4, 5, A4, A3, A2, and A1 on the Arduino for communication. The LCD will display real-time water levels and percentages of the four tanks.

### RTC Setup
The Real-Time Clock (RTC DS3231) is used to get the current time for scheduled SMS notifications at specific times (7:00 AM and 6:30 PM).

### Ultrasonic Sensor Setup
The ultrasonic sensors are connected to the following pins:
- Sensor 1: Trigger (Pin 6), Echo (Pin 7)
- Sensor 2: Trigger (Pin 9), Echo (Pin 8)
- Sensor 3: Trigger (Pin 10), Echo (Pin 11)
- Sensor 4: Trigger (Pin 12), Echo (Pin 13)

## Code Functionality

### `setup()` Function
- Initializes communication with the serial monitor, GSM module, RTC, and LCD.
- Sets the ultrasonic sensor pins as input/output.
- Checks if the RTC is connected properly; if not, halts the program.

### `loop()` Function
- Retrieves the current date and time from the RTC.
- Reads the water level from each of the four tanks using the ultrasonic sensors.
- Calculates the volume and percentage of water in each tank.
- Displays the water level information on the LCD.
- Sends SMS alerts if water levels drop below 25%, 50%, or 75%.
- Sends scheduled SMS notifications with water system status at 7:00 AM and 6:30 PM.
- Listens for incoming SMS to process water status requests.

### `Display()` Function
- Clears and updates the LCD with the current water levels, volumes, and percentage of each tank.

### `sendWaterStatusSms()` Function
- Constructs a message with the current water levels and sends it to a list of phone numbers.

### `sendSms()` Function
- Sends the SMS using AT commands to the GSM module. The function handles the message construction and communication with the GSM module.

### `serialEvent()` Function
- Processes incoming SMS messages. If a "water status" request is received, it triggers the system to send the current water system status via SMS.

## Tank Parameters
- **Tank 1, 2, 3, and 4**: Each tank has its own specific height, surface area, and total volume.
- **Thresholds**: 
  - 75%: High water level warning
  - 50%: Medium water level warning
  - 25%: Low water level warning

## SMS Alerts
- **Water Status**: When water levels drop below 75%, 50%, or 25%, an SMS is sent to the appropriate contact(s) with details about the tank's volume and percentage.
- **Scheduled Status Update**: The system sends an SMS with the water status at 7:00 AM and 6:30 PM every day.
- **SMS Commands**: Users can send "water status" via SMS to receive the current water levels and tank status.

## Connections
| Component              | Arduino Pin      |
|------------------------|------------------|
| GSM Module RX          | Pin 10           |
| GSM Module TX          | Pin 11           |
| LCD Display (RS)       | Pin 4            |
| LCD Display (EN)       | Pin 5            |
| LCD Display (D4-D7)    | A4, A3, A2, A1   |
| Sensor 1 Trigger       | Pin 6            |
| Sensor 1 Echo          | Pin 7            |
| Sensor 2 Trigger       | Pin 9            |
| Sensor 2 Echo          | Pin 8            |
| Sensor 3 Trigger       | Pin 10           |
| Sensor 3 Echo          | Pin 11           |
| Sensor 4 Trigger       | Pin 12           |
| Sensor 4 Echo          | Pin 13           |

## Troubleshooting
- **GSM Module Issues**: If the GSM module is not sending SMS, check the SIM card, ensure it has credit, and verify the AT commands are correctly sent.
- **LCD Issues**: Make sure the wiring is correct and the LCD is initialized properly in the code.
- **Sensor Issues**: Ensure the ultrasonic sensors are connected to the correct pins and functioning properly.

## License
This project is open source and released under the MIT License. Feel free to modify and distribute the code as needed.
