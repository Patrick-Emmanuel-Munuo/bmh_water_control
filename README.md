Here is the full updated `README.md` file with the added advantages, including the prevention of water overflow:

---

# Water Level Monitoring and Alert System At Block I

This project is a **Water Level Monitoring and Alert System** designed to monitor water levels in four tanks using ultrasonic sensors. The system calculates water volumes, displays the status on an LCD, and sends SMS alerts when water levels fall below predefined thresholds (75%, 50%, 25%) for each tank. Additionally, it provides scheduled SMS updates and can respond to SMS queries for real-time water tank status.

## Features

- **Real-Time Water Level Monitoring**: Measures water levels in four tanks using ultrasonic sensors.
- **SMS Alerts**: Sends SMS notifications when water levels drop below 75%, 50%, or 25%.
- **Scheduled Status Updates**: Sends scheduled water system status updates at 7:00 AM and 6:30 PM.
- **LCD Display**: Displays real-time tank volume and percentage on a 20x4 LCD screen.
- **Serial Monitor Output**: Prints the water tank status on the serial monitor for debugging.
- **SMS Command for Status**: Responds to SMS commands with the current water system status.

## Components Used

- **Arduino Board (e.g., Arduino Uno or similar)**
- **GSM Module (e.g., SIM800L, SIM900)**: For sending SMS alerts and receiving status requests.
- **Ultrasonic Sensors (e.g., HC-SR04)**: To measure water height and calculate water volume.
- **RTC Module (e.g., DS3231)**: For real-time clock functionality to send scheduled SMS updates.
- **LCD Display (e.g., 20x4 LCD)**: To display the water tank volume and percentage on the system.
- **Jumper Wires and PCB**: For connecting the components to the Arduino.

## Wiring Diagram

- **Ultrasonic Sensors**:
  - Sensor 1: Trigger pin → Pin 6, Echo pin → Pin 7
  - Sensor 2: Trigger pin → Pin 9, Echo pin → Pin 8
  - Sensor 3: Trigger pin → Pin 10, Echo pin → Pin 11
  - Sensor 4: Trigger pin → Pin 12, Echo pin → Pin 13
- **GSM Module**:
  - RX → Pin 10, TX → Pin 11
- **RTC DS3231 Module**: Uses I2C (SCL, SDA pins).
- **LCD Display**: Connected to pins (4, 5, A4, A3, A2, A1) for data and control.

## Installation and Setup

### Step 1: Install Libraries

Before uploading the code to the Arduino, you need to install the required libraries:

1. **SoftwareSerial**: For serial communication with the GSM module.
2. **LiquidCrystal**: To control the LCD screen.
3. **Wire**: For I2C communication with the RTC module.
4. **RTClib**: To interface with the RTC DS3231 module.

You can install these libraries using the Arduino Library Manager or by downloading them from GitHub.

### Step 2: Wiring the Components

- Connect the components according to the wiring diagram provided above. Make sure the ultrasonic sensor pins are connected to the correct digital pins on the Arduino and that the GSM module and RTC are connected properly.

### Step 3: Upload the Code

1. Open the Arduino IDE and load the provided code into the IDE.
2. Select the appropriate board and port under the **Tools** menu.
3. Click **Upload** to upload the code to your Arduino.

### Step 4: Configure the GSM Module

Make sure that your GSM module is properly configured to send and receive SMS. You will need to set the correct **phone numbers** in the `phoneNumbers[]` array to receive the SMS alerts.

### Step 5: Power the System

Once the code is uploaded, power the system by connecting it to a suitable power source (e.g., USB or battery pack). The system will start monitoring the water levels, displaying the status on the LCD, and sending SMS alerts when necessary.

## Code Explanation

### Initialization

- **GSM Module**: Communication with the GSM module is set up using the `SoftwareSerial` library to send SMS alerts.
- **RTC**: The RTC module is initialized to get the current date and time for scheduling SMS updates.
- **Ultrasonic Sensors**: These sensors measure the water height in each of the four tanks, which are then used to calculate the volume and percentage.
- **LCD**: The LCD displays the real-time water levels and volume of each tank.

### Main Loop

1. **Water Level Calculation**: The system calculates the water volume for each tank based on the sensor readings.
2. **Threshold Checking**: It checks if the water level falls below 75%, 50%, or 25% for each tank and sends SMS alerts accordingly.
3. **Scheduled Updates**: At 7:00 AM and 6:30 PM, the system sends a status update with the current water levels in all tanks.
4. **Incoming SMS Commands**: The system listens for incoming SMS commands (e.g., "water status") to send the current water system status.

### Functions

- **`Display()`**: Displays the water levels on the LCD.
- **`sendSms()`**: Sends an SMS to the specified phone number.
- **`sendWaterStatusSms()`**: Sends a status update with all tank volumes and percentages.
- **`serialEvent()`**: Processes incoming SMS messages to respond to the "water status" query.
- **`DisplaySerial()`**: Prints the water levels and volumes to the serial monitor.

## Future Enhancements

- **Remote Monitoring**: Add a web interface or a mobile app to remotely monitor the water levels and receive alerts.
- **Low Battery Alerts**: Implement a feature to alert users if the battery of the system or components (GSM/RTC) is running low.
- **Multiple Tank Support**: Extend the system to support more than four tanks by adding additional ultrasonic sensors and modifying the code accordingly.

## Troubleshooting

- **GSM Module Not Sending SMS**: Ensure that the GSM module has a stable network connection and that the SIM card has sufficient balance to send SMS.
- **Incorrect Sensor Readings**: Verify that the ultrasonic sensors are positioned properly and have a clear line of sight to the water surface.

## Cost Breakdown

### Materials

| **Item**                          | **Unit** | **Quantity** | **Rate (in currency)** | **Total Cost (in currency)** |
|------------------------------------|----------|--------------|------------------------|-----------------------------|
| Microcontroller                    | Pc       | 1            | 100,000                | 100,000                     |
| Ultrasonic Sensors                 | Pc       | 5            | 60,000                 | 300,000                     |
| Power Supply                       | Pc       | 1            | 10,000                 | 10,000                      |
| Connecting Wires                   | Pc       | 10           | 50,000                 | 500,000                     |
| PCB Circuit Board                  | Pc       | 1            | 15,000                 | 15,000                      |
| Water Proof Box                    | Pc       | 4            | 30,000                 | 120,000                     |
| LCD Display                        | Pc       | 1            | 60,000                 | 60,000                      |
| GSM Modem                          | Pc       | 1            | 150,000                | 150,000                     |
| UTP CAT 6 Wires                    | m        | 300          | 2,500                  | 750,000                     |
| Conduit Pipe                       | Pc       | 100          | 5,000                  | 500,000                     |
| Battery and Charger                | Pc       | 1            | 100,000                | 100,000                     |
| Relay                               | Pc       | 1            | 30,000                 | 30,000                      |
| Water Proof Glue                   | Pc       | 6            | 25,000                 | 150,000                     |
| Voltage Regulator & Auxiliary Components | Pc   | 1            | 25,000                 | 25,000                      |

### **Material Costs Summary**

- **Total Material Cost**: 2,810,000  
- **VAT**: 505,800  
- **Total Cost (Materials + VAT)**: 3,315,800

---

## Labor Charges

- **Labor Charges**: 828,950

---

## Total Project Cost

- **Total Cost (Materials + VAT + Labor)**: 4,144,750

---

## Advantages

- **Real-Time Monitoring**: Continuously tracks the water levels in four tanks, ensuring users can monitor the system at any time.
- **Automatic Alerts**: The system sends timely SMS alerts when water levels fall below critical thresholds (75%, 50%, 25%), reducing the risk of running dry.
- **Scheduled Updates**: The system automatically sends status updates twice a day (7:00 AM and 6:30 PM), keeping users informed about water levels without the need for constant manual checks.
- **SMS Command Functionality**: Users can query the system’s status in real time by simply sending an SMS, making it convenient to get updates remotely.
- **Cost-Effective**: The use of widely available and affordable components like ultrasonic sensors, GSM modules, and Arduino makes the system an economical solution for water level monitoring.
- **Easy Integration**: The system can be expanded to include additional sensors or features, such as multiple tank monitoring, low battery alerts, or remote access via a mobile app.
- **Prevention of Water Shortages**: By sending alerts when water levels are low, it helps prevent water shortages, ensuring tanks are refilled before running out of water.
- **User-Friendly Interface**: The LCD display shows clear, real-time information on the water level in each tank, offering a straightforward method for users to quickly assess the status.
- **Energy Efficient**: The system operates with low power consumption, making it ideal for installations in areas where energy efficiency is a concern.
- **Prevention of Water Overflow**: By continuously monitoring the water levels and sending timely alerts when levels are too low, the system can also help prevent overfilling or water overflow. With proper management and control over water usage, the system can ensure that tanks are not overfilled, thereby preventing damage to infrastructure or wastage of water.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

Let me know if you'd like any further tweaks or additions!