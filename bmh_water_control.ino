#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <Wire.h>
#include <RTClib.h>

// GSM Setup
SoftwareSerial mySerial(10, 11);  // RX, TX for GSM module
String serialString;

// Phone numbers stored in an array
String phoneNumbers[] = {
  "0625449295", // hod water halab mushi
  "0760449295", // director TSEMU Assenga
  "0775449295", // water monitor person Tech Daniel
  "0760449295" ,  // TSEMU kitengo Phone
  "0760449295"   // ED BMH 
};

// LCD Setup
LiquidCrystal Lcd(4, 5, A4, A3, A2, A1);  // LCD connections

// RTC Setup
RTC_DS3231 rtc;

// Pin Definitions
const int sensor1_trigPin = 6;
const int sensor1_echoPin = 7;
const int sensor2_trigPin = 9;
const int sensor2_echoPin = 8;
const int sensor3_trigPin = 10;
const int sensor3_echoPin = 11;
const int sensor4_trigPin = 12;
const int sensor4_echoPin = 13;

// Tank Parameters
const float emptyHeight1 = 12.33; // main tanks
const float emptyHeight2 = 12.33; // tank 1
const float emptyHeight3 = 12.33; // tank 2
const float emptyHeight4 = 12.33; // rainwater tank

// Surface Area on actual tank measurements
const float areaSurface1 = 12.33;
const float areaSurface2 = 12.33;
const float areaSurface3 = 12.33;
const float areaSurface4 = 12.33;

// Full Water Volume
const float volumeTotalTank1 = 12.33;
const float volumeTotalTank2 = 12.33;
const float volumeTotalTank3 = 12.33;
const float volumeTotalTank4 = 12.33;

// Water level thresholds (percentage)
// Water level thresholds (percentage)
const float thresholds1 = 75.0;  // 75%
const float thresholds2 = 50.0;  // 50%
const float thresholds3 = 25.0;  // 25%

// Flags to track previous alerts
bool lowWater75 = false;
bool lowWater50 = false;
bool lowWater25 = false;

float Volume1, Volume2, Volume3, Volume4;
float percentageTank1, percentageTank2, percentageTank3, percentageTank4;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  Lcd.begin(20, 4);  // Set LCD to 20x4
  // Initialize RTC
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);  // Halt if RTC is not found
  }
  // Initialize sensors
  pinMode(sensor1_trigPin, OUTPUT);
  pinMode(sensor1_echoPin, INPUT);
  pinMode(sensor2_trigPin, OUTPUT);
  pinMode(sensor2_echoPin, INPUT);
  pinMode(sensor3_trigPin, OUTPUT);
  pinMode(sensor3_echoPin, INPUT);
  pinMode(sensor4_trigPin, OUTPUT);
  pinMode(sensor4_echoPin, INPUT);
}

void loop() {
  // Get the current date and time from RTC
  DateTime now = rtc.now();

  // Read the water height levels for all tanks
  float tank1Level = getDistance(sensor1_trigPin, sensor1_echoPin);
  float tank2Level = getDistance(sensor2_trigPin, sensor2_echoPin);
  float tank3Level = getDistance(sensor3_trigPin, sensor3_echoPin);
  float tank4Level = getDistance(sensor4_trigPin, sensor4_echoPin);

  // Calculate volumes
  Volume1 = (emptyHeight1 - tank1Level) * areaSurface1;
  Volume2 = (emptyHeight2 - tank2Level) * areaSurface2;
  Volume3 = (emptyHeight3 - tank3Level) * areaSurface3;
  Volume4 = (emptyHeight4 - tank4Level) * areaSurface4;

  // Calculate percentage volumes
  percentageTank1 = (100*(volumeTotalTank1 - Volume1)) / volumeTotalTank1;
  percentageTank2 = (100*(volumeTotalTank2 - Volume2)) / volumeTotalTank2;
  percentageTank3 = (100*(volumeTotalTank3 - Volume3)) / volumeTotalTank3;
  percentageTank4 = (100*(volumeTotalTank4 - Volume4)) / volumeTotalTank4;

  // Display the tank volumes and percentages on the LCD
  Display();

  // Check if any tank is below 75%, 50%, or 25% and send an SMS
    // Check Tank 1
    if (percentageTank1 <= thresholds3 && !lowWater25) {
        sendSms(message, phoneNumbers[0]);
        lowWater25 = true;  // Set flag to avoid repeating alert
    } else if (percentageTank1 <= thresholds2 && !lowWater50) {
        sendSms(message, phoneNumbers[0]);
        lowWater50 = true;
    } else if (percentageTank1 <= thresholds1 && !lowWater75) {
        sendSms(message, phoneNumbers[0]);
        lowWater75 = true;
    }
    
    // Check Tank 2
    if (percentageTank2 <= thresholds3 && !lowWater25) {
        sendSms(message, phoneNumbers[1]);
        lowWater25 = true;
    } else if (percentageTank2 <= thresholds2 && !lowWater50) {
        sendSms(message, phoneNumbers[1]);
        lowWater50 = true;
    } else if (percentageTank2 <= thresholds1 && !lowWater75) {
        sendSms(message, phoneNumbers[1]);
        lowWater75 = true;
    }

    // Check Tank 3
    if (percentageTank3 <= thresholds3 && !lowWater25) {
        sendSms(message, phoneNumbers[2]);
        lowWater25 = true;
    } else if (percentageTank3 <= thresholds2 && !lowWater50) {
        sendSms(message, phoneNumbers[2]);
        lowWater50 = true;
    } else if (percentageTank3 <= thresholds1 && !lowWater75) {
        sendSms(message, phoneNumbers[2]);
        lowWater75 = true;
    }

    // Check Tank 4
    if (percentageTank4 <= thresholds3 && !lowWater25) {
        sendSms(message, phoneNumbers[3]);
        lowWater25 = true;
    } else if (percentageTank4 <= thresholds2 && !lowWater50) {
        sendSms(message, phoneNumbers[3]);
        lowWater50 = true;
    } else if (percentageTank4 <= thresholds1 && !lowWater75) {
        sendSms(message, phoneNumbers[3]);
        lowWater75 = true;
    }

    // Reset flags if water levels rise above thresholds
    if (percentageTank1 > thresholds1) lowWater75 = false;
    if (percentageTank1 > thresholds2) lowWater50 = false;
    if (percentageTank1 > thresholds3) lowWater25 = false;

    if (percentageTank2 > thresholds1) lowWater75 = false;
    if (percentageTank2 > thresholds2) lowWater50 = false;
    if (percentageTank2 > thresholds3) lowWater25 = false;

    if (percentageTank3 > thresholds1) lowWater75 = false;
    if (percentageTank3 > thresholds2) lowWater50 = false;
    if (percentageTank3 > thresholds3) lowWater25 = false;

    if (percentageTank4 > thresholds1) lowWater75 = false;
    if (percentageTank4 > thresholds2) lowWater50 = false;
    if (percentageTank4 > thresholds3) lowWater25 = false;
 
  // Send scheduled SMS at 7:00 AM and 6:30 PM with all tanks' volume and percentage
  if (now.hour() == 7 && now.minute() == 0) {
    sendWaterStatusSms("Scheduled Water System Status");
  }
  if (now.hour() == 18 && now.minute() == 30) {
    sendWaterStatusSms("Scheduled Water System Status");
  }

  // Process incoming SMS for status request
  serialEvent();

  delay(10000);  // Check every 10 seconds
}

void Display() {
  Lcd.clear();
  // Display Tank 1
  Lcd.setCursor(0, 0);
  Lcd.print("Tank 1: Vol: ");
  Lcd.print(Volume1, 2);
  Lcd.print("m^3: ");
  Lcd.print(percentageTank1 * 100, 1);
  Lcd.print("%");

  // Display Tank 2
  Lcd.setCursor(0, 1);
  Lcd.print("Tank 2: Vol: ");
  Lcd.print(Volume2, 2);
  Lcd.print("m^3: ");
  Lcd.print(percentageTank2 * 100, 1);
  Lcd.print("%");

  // Display Tank 3
  Lcd.setCursor(0, 2);
  Lcd.print("Tank 3: Vol: ");
  Lcd.print(Volume3, 2);
  Lcd.print("m^3: ");
  Lcd.print(percentageTank3 * 100, 1);
  Lcd.print("%");

  // Display Tank 4
  Lcd.setCursor(0, 3);
  Lcd.print("Tank 4: Vol: ");
  Lcd.print(Volume4, 2);
  Lcd.print("m^3: ");
  Lcd.print(percentageTank4 * 100, 1);
  Lcd.print("%");
}

void sendWaterStatusSms(String alertType) {
  // Construct message
  String message = alertType + ":\n";
  message += "Tank 1: Volume: " + String(Volume1, 3) + " m^3, " + String(percentageTank1 * 100, 2) + "%\n";
  message += "Tank 2: Volume: " + String(Volume2, 3) + " m^3, " + String(percentageTank2 * 100, 2) + "%\n";
  message += "Tank 3: Volume: " + String(Volume3, 3) + " m^3, " + String(percentageTank3 * 100, 2) + "%\n";
  message += "Tank 4: Volume: " + String(Volume4, 3) + " m^3, " + String(percentageTank4 * 100, 2) + "%\n";

  // Loop through phone numbers to send SMS
  for (const String& number : phoneNumbers) {
    sendSms(message, number);
  }
}

void sendSms(String text, String number) {
  mySerial.println("AT"); delay(200);
  mySerial.println("AT+CMGF=1"); delay(200);
  mySerial.println("AT+CMGS=\"" + number + "\"\r"); delay(200);
  mySerial.println(text); delay(300);
  mySerial.write(26);  // Send Ctrl+Z to indicate message end
  delay(400);
  if (mySerial.find("OK")) {
    Serial.println("SMS sent successfully.");
  } else {
    Serial.println("Failed to send SMS.");
  }
}

void serialEvent() {
  if (mySerial.available()) {
    String receivedMessage = mySerial.readString();
    receivedMessage.trim();  // Clean the message
    // If the received message is "water status", send the current status
    if (receivedMessage.indexOf("water status") != -1) {
      sendWaterStatusSms("Water System Status");
    }
  }
}
