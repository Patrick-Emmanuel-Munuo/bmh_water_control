Here’s a fresh `README.md` file, fully structured and with clear sections based on your project description:

---

# Water Level Monitoring and Alert System At Block I

## Overview

The **Water Level Monitoring and Alert System** is designed to monitor and manage the water levels in four tanks using ultrasonic sensors. This system sends SMS alerts when water levels fall below specific thresholds (75%, 50%, 25%), provides real-time updates via LCD display, and offers scheduled status notifications. Additionally, it includes SMS commands for querying the system’s status.

## Features

- **Real-Time Water Level Monitoring**: Monitors four tanks using ultrasonic sensors.
- **SMS Alerts**: Sends alerts when water levels drop below 75%, 50%, or 25%.
- **Scheduled Updates**: Sends daily updates at 7:00 AM and 6:30 PM.
- **LCD Display**: Displays water levels in each tank in percentage and volume.
- **SMS Command Functionality**: Responds to SMS requests for the water system status.
- **Overflow Prevention**: Helps prevent overfilling or overflow by sending alerts when levels exceed safe limits.
- **User-Friendly Interface**: Provides easy-to-read LCD status updates for users.

## Components Used

- **Arduino Board (e.g., Arduino Uno or similar)**
- **GSM Module (e.g., SIM800L, SIM900)**: For SMS communication.
- **Ultrasonic Sensors (e.g., HC-SR04)**: For measuring the water height in each tank.
- **RTC Module (e.g., DS3231)**: For time-based actions like scheduled SMS updates.
- **LCD Display (e.g., 20x4 LCD)**: Displays water level information.
- **Jumper Wires and PCB**: For connections between components.

## Wiring Diagram

- **Ultrasonic Sensors**:
  - Sensor 1: Trigger pin → Pin 6, Echo pin → Pin 7
  - Sensor 2: Trigger pin → Pin 9, Echo pin → Pin 8
  - Sensor 3: Trigger pin → Pin 10, Echo pin → Pin 11
  - Sensor 4: Trigger pin → Pin 12, Echo pin → Pin 13
- **GSM Module**:
  - RX → Pin 10, TX → Pin 11
- **RTC Module**: Uses I2C (SCL, SDA pins).
- **LCD Display**: Connected to pins (4, 5, A4, A3, A2, A1).

## Installation and Setup

### Step 1: Install Libraries

Before uploading the code to the Arduino, install the following libraries:
- **SoftwareSerial**: For GSM communication.
- **LiquidCrystal**: For controlling the LCD.
- **Wire**: For I2C communication with the RTC.
- **RTClib**: For interacting with the RTC DS3231.

Use the Arduino Library Manager to install these libraries or download them from GitHub.

### Step 2: Connect Components

Wire the components according to the diagram above. Ensure the ultrasonic sensors, GSM module, and RTC are connected to the correct pins.

### Step 3: Upload the Code

1. Open Arduino IDE.
2. Load the provided code into the IDE.
3. Select your board type and port under **Tools**.
4. Click **Upload** to send the code to the Arduino.

### Step 4: Configure GSM Module

Ensure your GSM module is properly set up with the correct phone numbers in the `phoneNumbers[]` array.

### Step 5: Power the System

Connect a suitable power source (e.g., USB or battery) to the system. It will start monitoring water levels, displaying them on the LCD, and sending alerts as necessary.

## Code Explanation

### Initialization

- **GSM Communication**: The system uses the `SoftwareSerial` library for sending SMS.
- **RTC Module**: Used to manage time-based actions for scheduled updates.
- **Ultrasonic Sensors**: Measure the height of water in the tanks.
- **LCD Display**: Shows real-time water levels and volume.

### Main Loop

1. **Water Level Calculation**: The ultrasonic sensors calculate the volume of water in each tank.
2. **Threshold Checking**: Checks if any tank water level falls below 75%, 50%, or 25% and sends SMS alerts.
3. **Scheduled Updates**: Sends water level status updates at 7:00 AM and 6:30 PM.
4. **Incoming SMS Commands**: Listens for incoming SMS commands like "water status" to provide updates.

### Key Functions

- **`sendSms()`**: Sends SMS alerts to predefined numbers.
- **`sendWaterStatusSms()`**: Sends the current water status of all tanks.
- **`Display()`**: Updates the LCD display with water levels.
- **`DisplaySerial()`**: Outputs water levels to the Serial Monitor for debugging.
- **`serialEvent()`**: Processes incoming SMS queries.

## Overflow Protection

To prevent overfilling, the system checks if the water levels exceed a critical threshold (e.g., 95%) for each tank. When the water level reaches this point, the system sends an overflow risk alert via SMS. 

### Example Code for Overflow Protection:
```cpp
void checkOverflowProtection() {
  if (percentageTank0 >= 95.0 && !overflowFlagTank0) {
    overflowFlagTank0 = true;
    sendWaterStatusSms("Tank 0 Overflow Risk! Level: " + String(percentageTank0) + "%");
  } else if (percentageTank0 < 90.0 && overflowFlagTank0) {
    overflowFlagTank0 = false;
  }
  // Repeat for other tanks
}
```

## Future Enhancements

- **Remote Monitoring**: Integrate a web interface or mobile app for remote monitoring and control.
- **Low Battery Alerts**: Alert users when system components (e.g., GSM, RTC) are running low on battery.
- **Multiple Tank Support**: Extend the system to manage more tanks.
- **Automated Pump Control**: Automate water pump activation based on tank levels.

## Troubleshooting

- **GSM Module Not Responding**: Ensure the SIM card is inserted properly and has enough balance. Check if the GSM module is in a location with adequate signal reception.
- **Incorrect Sensor Readings**: Verify the ultrasonic sensors are properly aligned and not obstructed by debris or tank structure.

## Cost Breakdown

REQUIRED WATER SYSTEM  CONTROLLER AT BLOCK I					
| **No.** | **Item**                           | **Unit** | **Quantity** | **Unit Cost (LKR)** | **Total Cost (LKR)** |
|---------|------------------------------------|----------|--------------|---------------------|----------------------|
| 1       | Microcontroller                    | Pc       | 1            | 100,000             | 100,000              |
| 2       | Ultrasonic Sensors                 | Pc       | 5            | 60,000              | 300,000              |
| 3       | Power Supply                       | Pc       | 1            | 10,000              | 10,000               |
| 4       | Connecting Wires                   | Pc       | 10           | 50,000              | 500,000              |
| 5       | PCB Circuit Board                  | Pc       | 1            | 15,000              | 15,000               |
| 6       | Water Proof Box                    | Pc       | 4            | 30,000              | 120,000              |
| 7       | LCD Display                        | Pc       | 1            | 60,000              | 60,000               |
| 8       | GSM Modem                          | Pc       | 1            | 150,000             | 150,000              |
| 9       | UTP CAT 6 Wires                    | m        | 300          | 2,500               | 750,000              |
| 10      | Conduit Pipe                       | Pc       | 100          | 5,000               | 500,000              |
| 11      | Battery and Charger                | Pc       | 1            | 100,000             | 100,000              |
| 12      | Relay                               | Pc       | 1            | 30,000              | 30,000               |
| 13      | Water Proof Glue                   | Pc       | 6            | 25,000              | 150,000              |
| 14      | Voltage Regulator & Auxiliary Components | Pc   | 1            | 25,000              | 25,000               |

### **Total Material Cost**: 2,810,000  
**VAT**: 505,800  
**Total Cost (Including VAT)**: 3,315,800

### Labor Charges: 828,950  
**Total Project Cost**: 4,144,750

## Advantages

- **Real-Time Monitoring**: Continuous tracking of water levels in four tanks.
- **Automatic Alerts**: Timely SMS alerts when levels drop below 75%, 50%, or 25%.
- **Scheduled Updates**: Get updates at 7:00 AM and 6:30 PM every day.
- **Overflow Prevention**: Alerts sent when tanks are at risk of overflowing.
- **Cost-Effective**: Affordable and widely available components.
- **Easy Integration**: Expandable system for more tanks or additional features like low battery alerts.
- **Prevention of Water Shortages and Overflow**: Alerts prevent running out of water or overfilling tanks.
- **User-Friendly Interface**: LCD display provides an easy way to check the system status.
- **Energy Efficient**: Operates with low power, making it ideal for remote installations.

## Code Explanation
Certainly! Let’s break down the code in detail and explain how it works with examples of outputs at each stage.

---

## **1. Libraries Used**

### **Libraries Included**
```cpp
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <Wire.h>
#include <RTClib.h>
```

- **SoftwareSerial.h**: Enables the use of serial communication on other digital pins, allowing for communication with devices like GSM modules. It allows us to control serial devices using any two available digital pins for RX and TX.
  
- **LiquidCrystal.h**: Provides functions to interface with an LCD screen. It allows us to display text and data such as water levels on an LCD.
  
- **Wire.h**: Allows communication with I2C devices, which is used to communicate with the Real-Time Clock (RTC) module.

- **RTClib.h**: Provides functions to interact with the RTC module. It helps us get the current date and time.

---

## **2. GSM Setup**

### **GSM Setup for SMS**
```cpp
SoftwareSerial mySerial(2, 3);  // RX, TX for GSM module
String serialString;
```

- **SoftwareSerial mySerial(2, 3)**: Initializes a software serial port on pins 2 (RX) and 3 (TX) for communicating with the GSM module.
  
- **String serialString**: Declares a string variable to hold the incoming data from the GSM module.

### Example Output:
- When the GSM module sends an SMS, we can capture the message in the `serialString` variable.

---

## **3. Phone Numbers**

### **Phone Numbers for Alerts**
```cpp
String phoneNumbers[] = {
  "0625449295", // hod water halab mushi
  "0760449295", // director TSEMU Assenga
  "0775449295", // water monitor person Tech Daniel
  "0760449295",  // TSEMU kitengo Phone
  "0760449295"   // ED BMH 
};
```

- The array **phoneNumbers[]** holds the phone numbers to which SMS alerts will be sent. These numbers represent people or roles (e.g., head of water management, director, etc.) who need to be informed about water levels or overflow.

### Example Output:
- If the water level in any tank crosses the threshold, an SMS will be sent to all numbers in the `phoneNumbers[]` array.

---

## **4. LCD Setup**

### **LCD Display Initialization**
```cpp
LiquidCrystal Lcd(4, 5, A4, A3, A2, A1);  // LCD connections
```

- **LiquidCrystal Lcd(4, 5, A4, A3, A2, A1)**: Configures the LCD by specifying the digital pins (4, 5, A4, A3, A2, A1) that connect to the LCD.

### Example Output:
- Displays the tank's volume and percentage on a 20x4 LCD. For example, when the water level is 70% in Tank 0, it might display:
  ```
  Tank 0: Vol: 2.56 m^3: 70.00%
  ```

---

## **5. RTC Setup**

### **RTC Setup for Timekeeping**
```cpp
RTC_DS3231 rtc;
```

- **RTC_DS3231 rtc**: Initializes the RTC module, which tracks the current time. This will help us send scheduled SMS messages at specific times.

### Example Output:
- We can read the time in the `loop()` function using:
  ```cpp
  DateTime now = rtc.now();
  ```
  Example output for the time would be:
  ```
  Current time: 07:00 AM
  ```

---

## **6. Tank Parameters**

### **Tank and Sensor Configuration**
```cpp
const int sensor0_trigPin = 4;
const int sensor0_echoPin = 5;
const int sensor1_trigPin = 6;
const int sensor1_echoPin = 7;
...
```

- **sensorX_trigPin**: Triggers the ultrasonic sensor to send a pulse.
- **sensorX_echoPin**: Receives the pulse back after hitting the water surface.

### **Tank Parameters**
```cpp
const float emptyHeight0 = 12.33; // roof tank1 level
const float volumeTotalTank0 = 12.33; // full volume for Tank 0
```

- **emptyHeight0**: Represents the height of the tank when it is empty.
- **volumeTotalTank0**: Represents the full volume capacity of Tank 0.

### Example Output:
- Based on ultrasonic sensor readings, the system will calculate the water level and volume for each tank. If the ultrasonic sensor detects a water level of 10 meters (out of 12.33 meters), it calculates the water volume.

---

## **7. Water Level Calculation**

### **Distance and Volume Calculation**
```cpp
float tank0Level = getDistance(sensor0_trigPin, sensor0_echoPin);
Volume0 = (emptyHeight0 - tank0Level) * areaSurface0;
percentageTank0 = (100 * (volumeTotalTank0 - Volume0)) / volumeTotalTank0;
```

- **getDistance()**: Measures the distance to the water surface using ultrasonic sensors. It returns the height of the water level in the tank.
  
- **Volume0 Calculation**: The volume of water is calculated by multiplying the difference between `emptyHeight0` and `tank0Level` by the surface area of the tank.

- **percentageTank0 Calculation**: The percentage of water in the tank is calculated by comparing the current volume to the total volume of the tank.

### Example Output:
- For **Tank 0**, if the sensor detects the water level to be 10 meters:
  ```
  Volume: (12.33 - 10.00) * 12.33 = 28.727 m^3
  Percentage: (100 * (12.33 - 28.727)) / 12.33 = 50%
  ```

---

## **8. Displaying Information on LCD**

### **Displaying Water Levels on LCD**
```cpp
Lcd.setCursor(0, 0);
Lcd.print("Tank 0: Vol: ");
Lcd.print(Volume0, 2);
Lcd.print(" m^3: ");
Lcd.print(percentageTank0, 1);
Lcd.print("%");
```

- **setCursor()**: Sets the position where the text will be displayed on the LCD.
- **print()**: Displays text or numeric values on the LCD.

### Example Output:
- LCD Output when Tank 0 is 50% full:
  ```
  Tank 0: Vol: 28.73 m^3: 50%
  ```

---

## **9. Sending SMS Alerts**

### **Sending SMS when Water Levels Cross Thresholds**
```cpp
sendWaterStatusSms("Scheduled Morning Water System Status");
```

- **sendWaterStatusSms()**: Sends the current water system status as an SMS to the phone numbers in the list.

### Example Output:
- If the water level in Tank 0 is below 50%, the system will send an SMS to all phone numbers:
  ```
  Tank 0: Volume: 28.73 m^3, 50.00%
  Tank 1: Volume: 32.12 m^3, 75.00%
  ```

---

## **10. Overflow Protection Logic**

### **Overflow Detection and SMS Alerts**
```cpp
if (percentageTank0 >= criticalLevel && !overflowFlagTank0) {
  overflowFlagTank0 = true;
  sendWaterStatusSms("Tank 0 Overflow Risk! Level: " + String(percentageTank0) + "%");
}
```

- **Overflow Protection**: If a tank's water level exceeds the critical level (e.g., 95%), it triggers the overflow flag and sends an alert.
- If the water level falls below a reset level (e.g., 90%), it resets the overflow flag.

### Example Output:
- If Tank 0's level is at 96%, an SMS will be sent:
  ```
  Tank 0 Overflow Risk! Level: 96%
  ```

---

## **11. Scheduled SMS**

### **Sending Scheduled SMS at Specific Times**
```cpp
if (now.hour() == 7 && now.minute() == 0) {
  sendWaterStatusSms("Scheduled Morning Water System Status");
}
if (now.hour() == 18 && now.minute() == 30) {
  sendWaterStatusSms("Scheduled Evening Water System Status");
}
```

- The system sends SMS updates at **7:00 AM** and **6:30 PM** every day. The message includes the status of all tanks.

### Example Output:
- At **7:00 AM**, an SMS will be sent with the status of all tanks:
  ```
  Tank 0: Volume: 28.73 m^3, 50.00%
  Tank 1: Volume: 32.12 m^3, 75.00%
  ```

---

### **Conclusion**
The system works by continuously measuring the water levels in various tanks, calculating their volumes, and displaying the information on an LCD. It also sends SMS alerts if any tank is approaching overflow levels, or if the water levels are low. The system is scheduled to send daily updates at specific times, ensuring that all stakeholders are informed about the water status.
## License
This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for more details.

---

Feel free to use this template as is, or modify it according to any additional information or changes you'd like to make! If you need further tweaks, feel free to ask.