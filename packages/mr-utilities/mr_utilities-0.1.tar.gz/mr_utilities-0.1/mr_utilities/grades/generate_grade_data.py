import random
import os
import argparse
import json
from faker import Faker
import sys

def generate_student_scores(file_path, num_of_students=500, mean=75, std_dev=10, num_grades=6, subjects='math,science,english,history,art,music', missing_data_prob=0.05, duplicate_prob=0.1):
    """
    Generates a JSON file with random student scores for multiple subjects, including random missing data and duplicates.
    Args:
        file_path (str): The path to the JSON file where the student scores will be saved.
        num_of_students (int, optional): The number of students to generate scores for. Defaults to 50.
        mean (float, optional): The mean score for the normal distribution. Defaults to 75.
        std_dev (float, optional): The standard deviation for the normal distribution. Defaults to 10.
        num_grades (int, optional): The number of classes to generate. Defaults to 4.
        subjects (list, optional): The list of subjects. Defaults to ['math', 'science', 'english'].
        missing_data_prob (float, optional): The probability of missing data for each field. Defaults to 0.1.
        duplicate_prob (float, optional): The probability of duplicating a student record. Defaults to 0.1.
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
    data = {grade_names: [] for grade_names in grade_names}

    # Generate student data for each class
    for class_name in grade_names:
        generate_students_for_class(data, class_name, num_of_students, num_grades, subjects, mean, std_dev, missing_data_prob, duplicate_prob, fake)

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the data to a JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data written to {file_path}")

def generate_students_for_class(data, class_name, num_of_students, num_grades, subjects, mean, std_dev, missing_data_prob, duplicate_prob, fake):
    students = []
    for _ in range(num_of_students // num_grades):
        name = generate_student_name(missing_data_prob, fake)
        sex = generate_student_sex(missing_data_prob)
        subject_scores = generate_subject_scores(subjects, mean, std_dev, missing_data_prob)
        average_score = calculate_average_score(subject_scores)
        total_score = calculate_total_score(subject_scores)
        student = {
            'name': name,
            'sex': sex,
            'subjects': subject_scores,
            'average_score': average_score,
            'total_score': total_score
        }
        students.append(student)
        data[class_name].append(student)

    # Introduce duplicates
    num_duplicates = int(len(students) * duplicate_prob)
    for _ in range(num_duplicates):
        duplicate_student = random.choice(students)
        data[class_name].append(duplicate_student)

def generate_student_name(missing_data_prob, fake):
    if random.random() < missing_data_prob:
        return None
    else:
        return f"{fake.first_name()} {fake.last_name()}"

def generate_student_sex(missing_data_prob):
    if random.random() < missing_data_prob:
        return None
    else:
        return random.choice(['M', 'F'])

def generate_subject_scores(subjects, mean, std_dev, missing_data_prob):
    subject_scores = {}
    for subject in subjects:
        if random.random() >= missing_data_prob:
            subject_scores[subject] = round(max(0, min(100, random.normalvariate(mean, std_dev))), 1)
    if random.random() < missing_data_prob:
        subject_scores = {}
    return subject_scores

def calculate_average_score(subject_scores):
    if subject_scores:
        return round(sum(subject_scores.values()) / len(subject_scores), 1)
    return None

def calculate_total_score(subject_scores):
    if subject_scores:
        return round(sum(subject_scores.values()), 1)
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate student scores and save to a JSON file.')
    parser.add_argument('--file_path', type=str, default='./data/grades_auto_generated.json', help='The path to the output JSON file.')
    parser.add_argument('--num_of_students', type=int, default=600, help='The number of students to generate.')
    parser.add_argument('--mean', type=float, default=75, help='The mean of the normal distribution.')
    parser.add_argument('--std_dev', type=float, default=10, help='The standard deviation of the normal distribution.')
    parser.add_argument('--num_grades', type=int, default=6, help='The number of grades to generate.')
    parser.add_argument('--subjects', type=str, default='math,science,english,history,art,biology,music', help='The subjects to generate scores for.')
    parser.add_argument('--missing_data_prob', type=float, default=0.1, help='The probability of missing data for each field.')
    parser.add_argument('--duplicate_prob', type=float, default=0.1, help='The probability of duplicating a student record.')
    args = parser.parse_args()
    generate_student_scores(args.file_path, args.num_of_students, args.mean, args.std_dev, args.num_grades, args.subjects, args.missing_data_prob, args.duplicate_prob)