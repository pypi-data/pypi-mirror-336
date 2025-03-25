import random
import os
import argparse
import json
from faker import Faker
import sys

def generate_student_scores(file_path, num_of_students=50, mean=75, std_dev=10, num_grades=4, subjects='math,science,english'):
    """
    Generates a JSON file with random student scores for multiple subjects.
    Args:
        file_path (str): The path to the JSON file where the student scores will be saved.
        num_of_students (int, optional): The number of students to generate scores for. Defaults to 50.
        mean (float, optional): The mean score for the normal distribution. Defaults to 75.
        std_dev (float, optional): The standard deviation for the normal distribution. Defaults to 10.
        num_grades (int, optional): The number of classes to generate. Defaults to 4.
        subjects (list, optional): The list of subjects. Defaults to ['math', 'science', 'english'].
    Returns:
        None
    The function creates a JSON file with the specified structure.
    """

    subjects = subjects.split(',')

    # Initialize Faker
    fake = Faker()

    # Generate random class names
    grade_names = [f"VG{random.randint(1, 3)}{chr(65 + i)}" for i in range(num_grades)]

    # Create a dictionary to hold the data
    data = {grade_name: [] for grade_name in grade_names}

    # Calculate the number of students for each grade with 10-50% difference
    remaining_students = num_of_students
    for i in range(num_grades - 1):
        num_students_in_grade = random.randint(int(num_of_students * 0.05), int(num_of_students * 0.15))
        remaining_students -= num_students_in_grade
        for _ in range(num_students_in_grade):
            subject_scores = {subject: round(max(0, min(100, random.normalvariate(mean, std_dev))), 1) for subject in subjects}
            student = {
                'name': f"{fake.first_name()} {fake.last_name()}",
                'subjects': subject_scores
            }
            data[grade_names[i]].append(student)

    # Assign remaining students to the last grade
    if remaining_students < 0:
        remaining_students = 28
    
    for _ in range(remaining_students):
        subject_scores = {subject: round(max(0, min(100, random.normalvariate(mean, std_dev))), 1) for subject in subjects}
        student = {
            'name': f"{fake.first_name()} {fake.last_name()}",
            'subjects': subject_scores
        }
        data[grade_names[-1]].append(student)

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the data to a JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data written to {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate student scores and save to a JSON file.')
    parser.add_argument('--file_path', type=str, default='./data/grades_auto_generated.json', help='The path to the output JSON file.')
    parser.add_argument('--num_of_students', type=int, default=50, help='The number of students to generate.')
    parser.add_argument('--mean', type=float, default=75, help='The mean of the normal distribution.')
    parser.add_argument('--std_dev', type=float, default=10, help='The standard deviation of the normal distribution.')
    parser.add_argument('--num_grades', type=int, default=14, help='The number of grades to generate.')
    parser.add_argument('--subjects', type=str, default='math,science,english', help='The subjects to generate scores for.')
    args = parser.parse_args()
    generate_student_scores(args.file_path, args.num_of_students, args.mean, args.std_dev, args.num_grades, args.subjects)