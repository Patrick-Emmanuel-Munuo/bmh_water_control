import mysql.connector
from flask import Flask, jsonify,request
import random
import threading
import time
from datetime import datetime  # <-- correct import
from flask_cors import CORS  # Importing flask_cors to enable CORS
import serial
# import package
import africastalking
from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()

# Initialize SDK
username = "YOUR_USERNAME"  
api_key = "YOUR_API_KEY"  


# Initialize Flask app and Limiter
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the client ip adress as json in console
@app.before_request
def log_request_info():
    try:
        client_ip = request.remote_addr
        now = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        print(f'{client_ip} - - [{now}] "{request.method} {request.path} HTTP/1.1"')
        # Log the request path and method
    except Exception as e:
        print(f"Error in log_request_info function: {e}")

# Pin Definitions for Ultrasonic Sensors and Corresponding Tank Details
# Array holding the details of each tank
tanks = [
    {
        "unique_id": "T000",   # Unique identifier for the tank
        "trig": 17,                             # Trigger pin for ultrasonic sensor
        "echo": 27,                             # Echo pin for ultrasonic sensor
        "name": 'Main Tank',                    # Name of the tank
        "area": 92.2,                           # Area of the tank (in m²)
        "empty_distance": 450,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 300000                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "T001",   # Unique identifier for the tank
        "trig": 22,                             # Trigger pin for ultrasonic sensor
        "echo": 23,                             # Echo pin for ultrasonic sensor
        "name": 'Rainwater Tank',                # Name of the tank
        "area": 590.25,                          # Area of the tank (in m²)
        "empty_distance": 355,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 726002                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "T002",   # Unique identifier for the tank
        "trig": 24,                             # Trigger pin for ultrasonic sensor
        "echo": 25,                             # Echo pin for ultrasonic sensor
        "name": 'Roof Tank 1',                   # Name of the tank
        "area": 60.3,                           # Area of the tank (in m²)
        "empty_distance": 450,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 240045                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "T003",   # Unique identifier for the tank
        "trig": 5,                              # Trigger pin for ultrasonic sensor
        "echo": 6,                              # Echo pin for ultrasonic sensor
        "name": 'Roof Tank 2',                   # Name of the tank
        "area": 40.35,                          # Area of the tank (in m²)
        "empty_distance": 455,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 160068                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "T004",   # Unique identifier for the tank
        "trig": 13,                             # Trigger pin for ultrasonic sensor
        "echo": 19,                             # Echo pin for ultrasonic sensor
        "name": 'Tank WTP1',                     # Name of the tank
        "area": 40.4,                           # Area of the tank (in m²)
        "empty_distance": 550,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 260060                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "T005",   # Unique identifier for the tank
        "trig": 26,                             # Trigger pin for ultrasonic sensor
        "echo": 12,                             # Echo pin for ultrasonic sensor
        "name": 'Tank WTP2',                     # Name of the tank
        "area": 34.5,                           # Area of the tank (in m²)
        "empty_distance": 555,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 260065                    # Total volume of the tank (in liters)
    }
]

# Phone numbers array
phone_numbers = [
    "+255625449295",  # developer Eng Patrick Munuo
   # "+255625449295",  # hod water Qs halab mushi
   # "+255760449295",  # director TSEMU Frank Assenga
   # "+255760449295",  # director Ag TSEMU Eng Mussa Kipende 
   # "+255775449295",  # water monitor person Tech Daniel Wesaka
    #"+255760449295",  # TSEMU kitengo Phonec\
    #"+255760449295"   # ED BMH
]

 
# Function to send water system status using GSM module to all phone numbers
def send_sms(message):
    try:
        for number in phone_numbers:
         # Serial communication setup for GSM module
         ser = serial.Serial('COM10', 9600)  # Replace with your GSM serial port
         ser.timeout = 1
         ser.write(b'AT\r')
         time.sleep(0.5)
         ser.write(b'AT+CMGF=1\r')  # Set SMS format to text
         time.sleep(0.5)
         ser.write(f'AT+CMGS="{number}"\r'.encode())  # Set recipient
         time.sleep(0.5)
         ser.write(message.encode())  # Send SMS body
         time.sleep(0.5)
         ser.write(bytes([26]))  # Send Ctrl+Z to indicate message end
         time.sleep(1)
         response = ser.read_all()
         if b'OK' in response:
            print(f"SMS sent successfully to {number}.")
         else:
            print(f"Failed to send SMS to {number}.")
    except Exception as e:
        print(f"Error in send_sms via gsm function: {e}")


# Function to send SMS using Africastalking
def send_sms_africastalking(message):
    try:
        for number in phone_numbers:
         # Initialize
         username = os.getenv("AFRICAS_TALKING_USERNAME") or "sandbox"  # Use "sandbox" for development in the test environment
         api_key = os.getenv("AFRICAS_TALKING_API_KEY") or "null"
         sender_id = os.getenv("AFRICAS_TALKING_SENDER_ID") or "sandbox"  # Use "sandbox" for development in the test environment
         print(f"username: {username}, api_key: {api_key}, sender_id: {sender_id}")
        
         # Initialize the SDK
         africastalking.initialize(username, api_key)
         # Initialize a service e.g. SMS
         sms = africastalking.SMS
         # # Use the service synchronously
         response = sms.send(message, [number], sender_id)
         # Initialize the SMS service
         print(response)
    except Exception as e:
        print(f"Error in send smm via africastalking api function: {e}")  

# Function to check and send SMS at scheduled times (7:00 AM and 6:30 PM)
def check_and_send_sms():
    try:
        while True:
            current_time = datetime.now()
            #print(f"Current time: {current_time}")
            # Check if it's exactly 7:00 AM
            if current_time.hour == 12 and current_time.minute == 45 and current_time.second == 0:
                send_sms_africastalking(f"Morning Water Status at {current_time}/n")
                time.sleep(2)  # Wait for 60 seconds to prevent multiple messages in the same minute
            # Check if it's exactly 6:30 PM
            elif current_time.hour == 18 and current_time.minute == 30 and current_time.second == 0:
                send_sms_africastalking(f"Evening Water Status at {current_time}/n")
                time.sleep(2)  # Wait for 60 seconds to prevent multiple messages in the same minute
            # Sleep for 1 second to check the time more frequently
            time.sleep(1)
    except Exception as e:
        print(f"Error in check_and_send_sms scheduled Water Status function: {e}")

# MySQL Database connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",         # Change to your MySQL username
            password="",         # Change to your MySQL password
            database="bmh_water_tank_data"
        )
    except Exception as e:
        print(f"Error in get_db_connection function: {e}")
        return None

# Function to get the water level parameters for each sensor (simulated)
def get_tank_data(sensor_num):
    try:
        # Access tank data from the array
        sensor = tanks[sensor_num]
        empty_distance = sensor['empty_distance']
        total_volume = sensor['total_volume']
        area = sensor['area']
        name = sensor['name']
        unique_id = sensor['unique_id']
        trig = sensor['trig']
        echo = sensor['echo']
        
        # calculate water air gap height
        height = random.uniform(299.0, 250.3)

        # calculate water volume/
        volume = (((empty_distance - height)/100) * area)*1000
        # calculate water percentage
        percentage = (volume / total_volume) * 100

        # Return all the parameters in the desired format
        return {
            "empty_height": empty_distance,
            "tank_name": name,
            "height": height,
            "water_level_percentage": percentage,
            "tank_total_volume": total_volume,
            "curent_water_volume": volume,
            "tank_unique_id": unique_id
        }

    except Exception as e:
        print(f"Error in get_tank_data for sensor {sensor_num}: {e}")
        return {"success": False, "message": f"Error retrieving data for sensor {sensor_num}: {str(e)}"}

# Overflow threshold (you can adjust based on the tank's design and your requirements)
OVERFLOW_THRESHOLD = 0.1  # For example, 10% over the empty distance.

# A dictionary to track overflow notifications for each tank
overflow_notified = {tank["unique_id"]: False for tank in tanks}

# Function to check for overflow in each tank and send SMS if overflow is detected
def check_for_overflow():
    try:
        while True:
            # Loop through all tanks and check their water levels
            for sensor_num in range(len(tanks)):  # Loop through each tank
                tank_data = get_tank_data(sensor_num)  # Get the tank data (including height and percentage)

                # Check if the water level is higher than the overflow threshold
                if tank_data["water_level_percentage"] >= (100 - OVERFLOW_THRESHOLD):
                    # If the tank hasn't already been notified, send an SMS and update the flag
                    if not overflow_notified[tank_data["tank_unique_id"]]:
                        message = f"Warning: {tank_data['tank_name']} is overflowing! Current water level: {tank_data['water_level_percentage']}%"
                        send_sms(message)  # Send the overflow notification via SMS
                        overflow_notified[tank_data["tank_unique_id"]] = True  # Mark that we've notified for this tank
                        print(f"Overflow notification sent for {tank_data['tank_name']}.")

                else:
                    # Reset the notification flag once the tank's water level is below the overflow threshold
                    if overflow_notified[tank_data["tank_unique_id"]]:
                        overflow_notified[tank_data["tank_unique_id"]] = False

            # Sleep for a short interval before checking again
            time.sleep(10)  # Check every 10 seconds (adjust as needed)
    except Exception as e:
        print(f"Error in check_for_overflow function: {e}")
        time.sleep(10)

# Function to insert data into MySQL every 60 seconds
def insert_data_every_minute():
    try:
        while True:
            connection = get_db_connection()
            if connection is None:
                time.sleep(60)
                continue
            cursor = connection.cursor()
            # Loop through each tank and insert the data
            for sensor_num, tank_data in enumerate(tanks):
                # Getting the data for each tank
                tank_data = get_tank_data(sensor_num)
                current_time = datetime.datetime.now()

                # Prepare the SQL statement
                query = """
                    INSERT INTO tank_levels (name, unique_id, empty_height, height, percentage, total_volume, volume, created_date, updated_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (
                    tank_data['tank_name'], 
                    tank_data['tank_unique_id'], 
                    tank_data['empty_height'], 
                    tank_data['height'], 
                    tank_data['water_level_percentage'], 
                    tank_data['tank_total_volume'], 
                    tank_data['curent_water_volume'],
                    current_time,  # created_date
                    current_time   # updated_date
                )
                # Execute the SQL statement
                cursor.execute(query, data)
                connection.commit()
            # Close cursor and connection
            cursor.close()
            connection.close()
            print(f"Succesful insert data to the database at {current_time}")
            # Wait for 30 minutes(1800seconds) before inserting again
            time.sleep(1800)
    except Exception as e:
        print(f"Error in insert_data_every_minute function: {e}")
        time.sleep(360)

# Start the data insertion thread
insert_thread = threading.Thread(target=insert_data_every_minute, daemon=True)
insert_thread.start()

# Start the check_and_send_sms thread
overflow_thread = threading.Thread(target=check_and_send_sms, daemon=True)
overflow_thread.start()

# Start the overflow checking thread
overflow_thread = threading.Thread(target=check_for_overflow, daemon=True)
overflow_thread.start()

#from datetime import timedelta

# Function to calculate the water consumption average for day, week, and month
def get_average_consumption():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500
            data = [
                {
                    "tank_name": "Main Tank",
                    "average_per_day": 500.0,
                    "average_per_week": 3500.0,
                    "average_per_month": 15000.0
                },
            ]
        return jsonify({
            "success": True,
            "message": data
        })

    except Exception as e:
        print(f"Error in get_average_consumption function: {e}")
        return jsonify({
            "success": False,
            "message": f"Failed to retrieve average consumption: {str(e)}"
        }), 500
    
@app.route('/consumption', methods=['GET'])
def get_average_consumption_route():
    try:
        return get_average_consumption()
    except Exception as e:
        print(f"Error in get_average_consumption_route function: {e}")
        return jsonify({
            "success": False,
            "message": f"Failed to retrieve average consumption: {str(e)}"
        }), 500

# Define the endpoint for retrieving water levels with rate limit
@app.route('/water_levels', methods=['GET'])
def get_water_levels():
    try:
        tank_data = []
        for sensor_num in range(len(tanks)):  # Loop through the array length
            tank_data.append(get_tank_data(sensor_num))  # Append each tank data to the list
        
        # Return the data in the requested format
        return jsonify({
            "success": True, 
            "message": tank_data
        })

    except Exception as e:
        print(f"Error in get_water_levels function: {e}")
        return jsonify({
            "success": False, 
            "message": f"Failed to retrieve water levels: {str(e)}"
        }), 500

# Define the endpoint for retrieving read data in the database
@app.route('/read', methods=['GET'])
def read_data():
    try:
        data = []
        table = "tank_levels"
        connection = get_db_connection()
        if connection is None:
            return jsonify({
                "success": False, 
                "message": "Database connection failed"
            }), 500
        
        cursor = connection.cursor()
        # Prepare the SQL statement
        query = f"SELECT * FROM {table} ORDER BY created_date DESC"
        # Execute the SQL statement
        cursor.execute(query)
        # Fetch all the data
        records = cursor.fetchall()
        # Loop through each record and append to the data list
        for record in records:
            data.append({
                "id": record[0],
                "name": record[1],
                "unique_id": record[2],
                "empty_height": record[3],
                "height": record[4],
                "percentage": record[5],
                "total_volume": record[6],
                "volume": record[7],
                "created_date": record[8],
                "updated_date": record[9]
            })
        # Return the data in the requested format
        return jsonify({
            "success": True, 
            "message": data
        })

    except Exception as e:
        print(f"Error in read_data function: {e}")
        return jsonify({
            "success": False, 
            "message": f"Failed to retrieve read data in the database : {str(e)}"
        }), 500

# Run the Flask app
def run_flask_app():
    try:
        app.run(host='0.0.0.0', port=2010, debug=False)
    except Exception as e:
        print(f"Error in run_flask_app function: {e}")

if __name__ == "__main__":
    try:
        #run_flask_app()
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()

        #sms_thread = threading.Thread(target=check_and_send_sms, daemon=True)
       # sms_thread.start()

        # Keep the main thread alive to run both Flask and the SMS checking loop
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error in main block: {e}")
        time.sleep(1)