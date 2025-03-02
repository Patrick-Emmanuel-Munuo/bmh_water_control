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

# Pin Definitions for Ultrasonic Sensors and corresponding tank names (tanks as an array)
tanks = [
    {"unique_id": "67b17fce9e034bfffaa51f48", 'trig': 17, 'echo': 27, 'name': 'Main Tank', 'area': 32.2, 'empty_distance': 30, 'total_volume': 2100},
    {"unique_id": "67b17fce9e034bfffaa51f49", 'trig': 22, 'echo': 23, 'name': 'Rainwater Tank', 'area': 20.25, 'empty_distance': 35, 'total_volume': 3262},
    {"unique_id": "67b17fce9e034bfffaa51f50", 'trig': 24, 'echo': 25, 'name': 'Roof Tank 1', 'area': 40.3, 'empty_distance': 40, 'total_volume': 2445},
    {"unique_id": "67b17fce9e034bfffaa51f51", 'trig': 5, 'echo': 6, 'name': 'Roof Tank 2', 'area': 30.35, 'empty_distance': 45, 'total_volume': 1668},
    {"unique_id": "67b17fce9e034bfffaa51f52", 'trig': 13, 'echo': 19, 'name': 'Tank WTP1', 'area': 40.4, 'empty_distance': 50, 'total_volume': 2660},
    {"unique_id": "67b17fce9e034bfffaa51f53", 'trig': 26, 'echo': 12, 'name': 'Tank WTP2', 'area': 34.5, 'empty_distance': 55, 'total_volume': 2665}
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

# Function to send water system status to all phone numbers
def send_water_status_sms(message):
    for number in phone_numbers:
        send_sms(message, number)

# Function to check and send SMS at scheduled times (7:00 AM and 6:30 PM)
def check_and_send_sms():
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

# MySQL Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Change to your MySQL username
        password="",         # Change to your MySQL password
        database="bmh_water_tank_data"
    )

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
        height = random.uniform(0.0, 4.3)

        # calculate water volume
        volume = (empty_distance - height) * area
        # calculate water percentage
        percentage = ((total_volume - volume) / total_volume) * 100

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
        # Return structured error message if any error occurs
        print(f"Error in get_tank_data for sensor {sensor_num}: {e}")
        return {"success": False, "message": f"Error retrieving data for sensor {sensor_num}: {str(e)}"}

# Function to insert data into MySQL every 60 seconds
def insert_data_every_minute():
    while True:
        try:
            connection = get_db_connection()
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
            print(f"Error in insert_data_every_minute: {e}")
            time.sleep(60)

# Start the data insertion thread
insert_thread = threading.Thread(target=insert_data_every_minute, daemon=True)
insert_thread.start()

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
        # Return structured error message in case of failure
        print(f"Error in get_water_levels: {e}")
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
        # Return structured error message in case of failure
        print(f"Error in read data in the database: {e}")
        return jsonify({
            "success": False, 
            "message": f"Failed to retrieve read data in the database : {str(e)}"
        }), 500
# Run the Flask app
def run_flask_app():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    #run_flask_app()
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()

    sms_thread = threading.Thread(target=check_and_send_sms, daemon=True)
    sms_thread.start()

    # Keep the main thread alive to run both Flask and the SMS checking loop
    while True:
        time.sleep(1)
