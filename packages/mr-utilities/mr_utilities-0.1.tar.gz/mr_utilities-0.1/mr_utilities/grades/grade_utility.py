import csv
import random
import datetime
import json

def load_grade_data(filepath):
    """
    Loads grade data from a JSON file.
    Args:
        filepath (str): The path to the JSON file containing grade data.
    Returns:
        dict: The grade data loaded from the file if successful.
        None: If the file is not found, is not a valid JSON file, or an unexpected error occurs.
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON file.
        Exception: For any other unexpected errors.
    """
    
    try:
        with open(filepath, 'r') as file:
            grade_data = json.load(file)
            return grade_data
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {filepath} is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
def flatten_grade_data(data):
    """
    Flattens nested grade data into a list of dictionaries with subject scores.
    Args:
        data (dict): A dictionary where keys are grade names and values are lists of student dictionaries.
                     Each student dictionary contains 'name' and 'subjects' keys.
                     'subjects' is a dictionary where keys are subject names and values are scores.
    Returns:
        list: A list of dictionaries where each dictionary represents a student with their grade, name, 
              and subject scores. Subject scores are represented with keys in the format 'subject.<subject_name>'.
    """
    flattened_data = []
    for grade_name, students in data.items():
        for student in students:
            flattened_student = {'grade': grade_name, 'name': student['name'], 'sex': student['sex']}
            for subject, score in student['subjects'].items():
                flattened_student[f'subject.{subject}'] = score
            flattened_data.append(flattened_student)
    return flattened_data    
    

# Generate a random date
def random_date():
    year = random.randint(2018, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)

# Generate a random time
def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.time(hour, minute, second)

# Generate a random temperature
def random_temperature():
    return random.uniform(-10, 40)

# Generate a random humidity
def random_humidity():
    return random.uniform(0, 100)

# Generate a random pressure
def random_pressure():
    return random.uniform(900, 1100)

# Generate a random wind speed
def random_wind_speed():
    return random.uniform(0, 100)

# Generate a random wind direction
def random_wind_direction():
    return random.randint(0, 360)

# Generate a random rain
def random_rain():
    return random.uniform(0, 100)   

# Generate a random solar radiation
def random_solar_radiation():
    return random.uniform(0, 1000)

# Generate a random uv index
def random_uv_index():
    return random.randint(0, 10)

def generate_temp_data(file_name, number_of_rows):
    """
    Generates synthetic temperature data and saves it to a CSV file.
    Parameters:
    file_name (str): The name of the CSV file to save the data.
    number_of_rows (int): The number of rows of data to generate.
    The generated data includes the following columns:
    - date: Randomly generated date.
    - time: Randomly generated time.
    - temperature: Randomly generated temperature.
    - humidity: Randomly generated humidity.
    - pressure: Randomly generated pressure.
    - wind speed: Randomly generated wind speed.
    - wind direction: Randomly generated wind direction.
    - rain: Randomly generated rain amount.
    - solar radiation: Randomly generated solar radiation.
    - uv index: Randomly generated UV index.
    Some values in the data will be randomly set to None to simulate missing values.
    The data is saved in a CSV file with the specified file name.
    """

    print(file_name)
    # Now, create test data to be saved in a csv file
    data = []
    for i in range(number_of_rows):
        date = random_date()
        time = random_time()
        temperature = random_temperature()
        humidity = random_humidity()
        pressure = random_pressure()
        wind_speed = random_wind_speed()
        wind_direction = random_wind_direction()
        rain = random_rain()
        solar_radiation = random_solar_radiation()
        uv_index = random_uv_index()
        data.append([date, time, temperature, humidity, pressure, wind_speed, wind_direction, rain, solar_radiation, uv_index])
        
    # Add missing values (50% of the total values)
    total_values = number_of_rows * 10  # Total number of values in the dataset
    num_missing_values = total_values // 2  # 50% of the total values

    for _ in range(num_missing_values):
        row_idx = random.randint(0, number_of_rows - 1)
        col_idx = random.randint(0, 9)
        data[row_idx][col_idx] = None
    
    # Save the data in a csv file
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'time', 'temperature', 'humidity', 'pressure', 'wind speed', 'wind direction', 'rain', 'solar radiation', 'uv index'])
        for row in data:
            writer.writerow(row)