import mysql.connector
from flask import Flask, jsonify
import random
import threading
import time
import datetime
from flask_cors import CORS  # Importing flask_cors to enable CORS
import serial


# Initialize Flask app and Limiter
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Pin Definitions for Ultrasonic Sensors and Corresponding Tank Details

# Array holding the details of each tank
# Array holding the details of each tank
tanks = [
    {
        "unique_id": "67b17fce9e034bfffaa51f48",   # Unique identifier for the tank
        "trig": 17,                             # Trigger pin for ultrasonic sensor
        "echo": 27,                             # Echo pin for ultrasonic sensor
        "name": 'Main Tank',                    # Name of the tank
        "area": 32.2,                           # Area of the tank (in m²)
        "empty_distance": 450,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 300000                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "67b17fce9e034bfffaa51f49",   # Unique identifier for the tank
        "trig": 22,                             # Trigger pin for ultrasonic sensor
        "echo": 23,                             # Echo pin for ultrasonic sensor
        "name": 'Rainwater Tank',                # Name of the tank
        "area": 20.25,                          # Area of the tank (in m²)
        "empty_distance": 355,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 726002                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "67b17fce9e034bfffaa51f50",   # Unique identifier for the tank
        "trig": 24,                             # Trigger pin for ultrasonic sensor
        "echo": 25,                             # Echo pin for ultrasonic sensor
        "name": 'Roof Tank 1',                   # Name of the tank
        "area": 60.3,                           # Area of the tank (in m²)
        "empty_distance": 450,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 240045                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "67b17fce9e034bfffaa51f51",   # Unique identifier for the tank
        "trig": 5,                              # Trigger pin for ultrasonic sensor
        "echo": 6,                              # Echo pin for ultrasonic sensor
        "name": 'Roof Tank 2',                   # Name of the tank
        "area": 40.35,                          # Area of the tank (in m²)
        "empty_distance": 455,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 160068                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "67b17fce9e034bfffaa51f52",   # Unique identifier for the tank
        "trig": 13,                             # Trigger pin for ultrasonic sensor
        "echo": 19,                             # Echo pin for ultrasonic sensor
        "name": 'Tank WTP1',                     # Name of the tank
        "area": 40.4,                           # Area of the tank (in m²)
        "empty_distance": 550,                   # Distance at which the tank is considered empty (in cm)
        "total_volume": 260060                    # Total volume of the tank (in liters)
    },
    {
        "unique_id": "67b17fce9e034bfffaa51f53",   # Unique identifier for the tank
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
    "0625449295",  # hod water halab mushi
    "0760449295",  # director TSEMU Assenga
    "0775449295",  # water monitor person Tech Daniel
    "0760449295",  # TSEMU kitengo Phone
    "0760449295"   # ED BMH
]

# Serial communication setup for GSM module
ser = serial.Serial('COM10', 9600)  # Replace with your GSM serial port
ser.timeout = 1

# Function to send SMS using GSM module
def send_sms(text, number):
    try:
        ser.write(b'AT\r')
        time.sleep(0.5)
        ser.write(b'AT+CMGF=1\r')  # Set SMS format to text
        time.sleep(0.5)
        ser.write(f'AT+CMGS="{number}"\r'.encode())  # Set recipient
        time.sleep(0.5)
        ser.write(text.encode())  # Send SMS body
        time.sleep(0.5)
        ser.write(bytes([26]))  # Send Ctrl+Z to indicate message end
        time.sleep(1)
        response = ser.read_all()
        if b'OK' in response:
            print(f"SMS sent successfully to {number}.")
        else:
            print(f"Failed to send SMS to {number}.")
    except Exception as e:
        print(f"Error in send_sms function: {e}")

# Function to send water system status to all phone numbers
def send_water_status_sms(message):
    try:
        for number in phone_numbers:
            send_sms(message, number)
    except Exception as e:
        print(f"Error in send_water_status_sms function: {e}")

# Function to check and send SMS at scheduled times (7:00 AM and 6:30 PM)
def check_and_send_sms():
    try:
        while True:
            current_time = datetime.datetime.now()
            # Check if it's exactly 7:00 AM
            if current_time.hour == 7 and current_time.minute == 0 and current_time.second == 0:
                send_water_status_sms("Scheduled Morning Water System Status")
                time.sleep(2)  # Wait for 60 seconds to prevent multiple messages in the same minute
            # Check if it's exactly 6:30 PM
            elif current_time.hour == 18 and current_time.minute == 30 and current_time.second == 0:
                send_water_status_sms("Scheduled Evening Water System Status")
                time.sleep(2)  # Wait for 60 seconds to prevent multiple messages in the same minute
            # Sleep for 1 second to check the time more frequently
            time.sleep(1)
    except Exception as e:
        print(f"Error in check_and_send_sms function: {e}")

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
        height = random.uniform(229.0, 350.3)

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
                        send_water_status_sms(message)  # Send the overflow notification via SMS
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
            # Wait for 60 seconds before inserting again
            time.sleep(60)
    except Exception as e:
        print(f"Error in insert_data_every_minute function: {e}")
        time.sleep(60)

# Start the data insertion thread
insert_thread = threading.Thread(target=insert_data_every_minute, daemon=True)
insert_thread.start()

# Start the overflow checking thread
overflow_thread = threading.Thread(target=check_for_overflow, daemon=True)
overflow_thread.start()
from datetime import timedelta

# Function to calculate the water consumption average for day, week, and month
def get_average_consumption():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = connection.cursor()

        # Get the total consumption and time period information
        query = """
            SELECT
                name,
                SUM(volume) AS total_volume,
                MIN(created_date) AS start_date,
                MAX(created_date) AS end_date
            FROM tank_levels
            GROUP BY name
        """
        cursor.execute(query)
        records = cursor.fetchall()

        # Initialize data structure to store the average consumption per period
        consumption_data = {}

        # For each tank, calculate the average consumption for day, week, and month
        for record in records:
            name = record[0]
            total_volume = record[1]
            start_date = record[2]
            end_date = record[3]

            # Calculate the duration in days, weeks, and months
            total_days = (end_date - start_date).days
            total_weeks = total_days // 7
            total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

            # Avoid division by zero if no records are available
            if total_days == 0: total_days = 1
            if total_weeks == 0: total_weeks = 1
            if total_months == 0: total_months = 1

            # Calculate average consumption
            avg_per_day = total_volume / total_days
            avg_per_week = total_volume / total_weeks
            avg_per_month = total_volume / total_months

            consumption_data[name] = {
                "average_per_day": avg_per_day,
                "average_per_week": avg_per_week,
                "average_per_month": avg_per_month
            }

        cursor.close()
        connection.close()

        return jsonify({
            "success": True,
            "message": consumption_data
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
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"Error in run_flask_app function: {e}")

if __name__ == "__main__":
    try:
        #run_flask_app()
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()

        sms_thread = threading.Thread(target=check_and_send_sms, daemon=True)
        sms_thread.start()

        # Keep the main thread alive to run both Flask and the SMS checking loop
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error in main block: {e}")
        time.sleep(1)