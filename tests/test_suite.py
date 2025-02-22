#!/usr/bin/env python3.11

import random
import time
from mysql.connector import pooling

pool = pooling.MySQLConnectionPool(
    pool_name='pool',
    pool_size=32,
    user='py',
    host='localhost',
    database='university',
    password='xKHOxyThyC7u8f',
    port='3306',
    connect_timeout=3600,
    )
department_list = []
course_list = []
address_list = []
female_names = []
male_names = []
last_names = []
student_max: int
teacher_max: int
classes_max: int

connector = pool.get_connection()
cursor = connector.cursor()

cursor.execute('SELECT * FROM departments')
results = cursor.fetchall()
if not results:
    print('Failed to retrieve table department!')
    exit(1)
for row in results:
    department_list.append(row[0])

cursor.execute('SELECT * FROM courses')
results = cursor.fetchall()
if not results:
    print('Failed to retrieve tables course!')
    exit(1)
for row in results:
    course_list.append(row)

cursor.execute('SELECT * FROM addresses')
results = cursor.fetchall()
if not results:
    print('Failed to retrieve table addresses!')
    exit(1)
for row in results:
    address_list.append(row)

cursor.execute('SELECT * FROM female_names')
results = cursor.fetchall()
if not results:
    print('Failed to retrieve table female_names!')
    exit(1)
for row in results:
    female_names.append(row[0])

cursor.execute('SELECT * FROM male_names')
results = cursor.fetchall()
if not results:
    print('Failed to retrieve table male_names!')
    exit(1)
for row in results:
    male_names.append(row[0])

cursor.execute('SELECT * FROM last_names')
results = cursor.fetchall()
if not results:
    print('Failed to retrieve table last_names!')
    exit(1)
for row in results:
    last_names.append(row[0])

cursor.execute('SELECT MAX(id) FROM students')
result = cursor.fetchone()[0]
if not result:
    print('Failed to retrieve max from students!')
    exit(1)
else:
    student_max = result

cursor.execute('SELECT MAX(id) FROM teachers')
result = cursor.fetchone()[0]
if not result:
    print('Failed to retrieve max from tecahers!')
    exit(1)
else:
    teacher_max = result

cursor.execute('SELECT MAX(class_id) FROM classes')
result = cursor.fetchone()[0]
if not result:
    print('Failed to retrieve max from classes!')
    exit(1)
else:
    classes_max = result

connector.close()

def sequential_index():
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(3000):
        cursor.execute(
            f'SELECT * FROM students WHERE id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(3000):
        cursor.execute(
            f'SELECT * FROM students_contact WHERE id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(3000):
        cursor.execute(
            f'SELECT * FROM students_address WHERE id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(3000):
        cursor.execute(
            f'SELECT * FROM students JOIN students_address on students.id = students_address.id JOIN students_contact on students.id = students_contact.id WHERE students.id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(500):
        cursor.execute(
            f'SELECT * FROM teachers WHERE id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    for _ in range(500):
        cursor.execute(
            f'SELECT * FROM teachers_contact WHERE id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    for _ in range(500):
        cursor.execute(
            f'SELECT * FROM teachers_address WHERE id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    print(f'Indexed lookup: {time.time() - then:.2f} seconds')

def string_matching():
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name LIKE \"{random.choice(male_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name LIKE \"{random.choice(female_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name LIKE \"{random.choice(male_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name LIKE \"{random.choice(female_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    print(f'String matching test: {time.time() - then:.2f} seconds')

def regex_matching():
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name RLIKE \"{random.choice(male_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name RLIKE \"{random.choice(female_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name RLIKE \"{random.choice(male_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(5):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name RLIKE \"{random.choice(female_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    print(f'Regex matching test: {time.time() - then:.2f} seconds')

if __name__ == '__main__':
    sequential_index()
    string_matching()
    regex_matching()
