import random
import os
import argparse

def generate_experimental_data(file_path, num_of_measurements=50, min_height=1, max_height=5):
    # Generate measured data for a ball to fall from different heights.
    data = []
    for i in range(num_of_measurements):
        height = random.randint(min_height, max_height)
        
        # add some noise to the measurement
        measurement = {
            'measurement_id': i,
            'height': height,
            'time_to_fall': (2 * height / 9.81) ** 0.5 + random.uniform(-0.1, 0.1)
        }
        data.append(measurement)        

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the list of dictionaries to a CSV file
    with open(file_path, 'w') as f:
        f.write('measurement_id,height,time_to_fall\n')
        for row in data:
            f.write(f"{row['measurement_id']},{row['height']},{row['time_to_fall']}\n")

    print(f"Data written to {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate measurements and save to a CSV file.')
    parser.add_argument('file_path', type=str, help='The path to the output CSV file.')
    parser.add_argument('num_of_measurements', type=int, help='The number of measurements to generate.')
    parser.add_argument('min_height', type=int, help='The minimum height of the ball.')
    parser.add_argument('max_height', type=int, help='The maximum height of the ball.')
    args = parser.parse_args()
    generate_experimental_data(args.file_path, args.num_of_measurements, args.min_height, args.max_height)