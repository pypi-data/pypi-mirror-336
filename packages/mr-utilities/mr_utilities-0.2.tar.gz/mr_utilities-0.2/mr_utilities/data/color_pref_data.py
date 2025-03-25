import random
import os
import argparse
from faker import Faker

def generate_student_color_pref(file_path, num_of_students=50):
    # Initialize Faker
    fake = Faker()

    # Create a list of dictionaries with student_id, student last name, student first name, and score
    students = []
    
    # List of standard colors
    colors = ['Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Black', 'White']
    
    for i in range(num_of_students):
        
        favorite_color = random.choice(colors)
        
        student = {
            'student_id': i,
            'last_name': fake.last_name(),
            'first_name': fake.first_name(),
            'favorite_color': favorite_color
        }
        students.append(student)

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the list of dictionaries to a CSV file
    with open(file_path, 'w') as f:
        f.write('student_id,last_name,first_name,favorite_color\n')
        for student in students:
            f.write(f"{student['student_id']},{student['last_name']},{student['first_name']},{student['favorite_color']}\n")

    print(f"Data written to {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate student color preferences and save to a CSV file.')
    parser.add_argument('file_path', type=str, help='The path to the output CSV file.')
    parser.add_argument('num_of_students', type=int, help='The number of students to generate.')
    args = parser.parse_args()
    generate_student_color_pref(args.file_path, args.num_of_students)