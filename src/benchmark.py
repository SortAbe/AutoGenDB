#!/usr/bin/env python3.11

import datetime
import json
import random
import subprocess
import time
from mysql.connector import pooling

pool = pooling.MySQLConnectionPool(
    pool_name='pool',
    pool_size=16,
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
test_results = {}


def offset():
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global student_max
    global teacher_max
    global classes_max
    global test_results
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

def parameter_variables():
    global test_results
    try:
        size = subprocess.check_output(['du', '-s', '/var/lib/mysql'], text=True).split('\t')[0]
        test_results['var_lib_mysql_size'] = size
    except subprocess.CalledProcessError as error:
        print(error)
    try:
        with open('results.json', 'r') as json_file:
            result_list = json.load(json_file)
    except FileNotFoundError as error:
        result_list = {}
        result_list['results'] = []
    result_list['results'].append(test_results)
    with open('results.json', 'w') as json_file:
        json.dump(result_list, json_file, indent=4)

def index_lookup():
    global student_max
    global teacher_max
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM students WHERE id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM students_contact WHERE id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM students_address WHERE id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM teachers WHERE id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM teachers_contact WHERE id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM teachers_address WHERE id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    total_time = time.time() - then
    print(f'Indexed lookup: {total_time:.2f} seconds')
    test_results['index_lookup'] = total_time
    connection.close()

def joined_index_lookup():
    global student_max
    global teacher_max
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM students JOIN students_address on students.id = students_address.id JOIN students_contact on students.id = students_contact.id WHERE students.id = {random.randint(0, student_max)};'
        )
        cursor.fetchone()
    for _ in range(2000):
        cursor.execute(
            f'SELECT * FROM teachers JOIN teachers_address on teachers.id = teachers_address.id JOIN teachers_contact on teachers.id = teachers_contact.id WHERE teachers.id = {random.randint(0, teacher_max)};'
        )
        cursor.fetchone()
    total_time = time.time() - then
    print(f'Joined indexed lookup: {total_time:.2f} seconds')
    test_results['join_index_lookup'] = total_time
    connection.close()

def string_lookup():
    global female_names
    global male_names
    global last_names
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name LIKE \"{random.choice(male_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name LIKE \"{random.choice(female_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name LIKE \"{random.choice(male_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name LIKE \"{random.choice(female_names)}\" AND last_name LIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    total_time = time.time() - then
    print(f'String lookup: {total_time:.2f} seconds')
    test_results['string_lookup'] = total_time
    connection.close()

def regex_lookup():
    global female_names
    global male_names
    global last_names
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    then = time.time()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name RLIKE \"{random.choice(male_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM students WHERE first_name RLIKE \"{random.choice(female_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name RLIKE \"{random.choice(male_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    for _ in range(2):
        cursor.execute(
            f'SELECT * FROM teachers WHERE first_name RLIKE \"{random.choice(female_names)}\" AND last_name RLIKE \"{random.choice(last_names)}\" LIMIT 1;'
        )
        cursor.fetchone()
    total_time = time.time() - then
    print(f'Regex lookup: {total_time:.2f} seconds')
    test_results['regex_lookup'] = total_time
    connection.close()

def derived_queries():
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    queries = [
        'SELECT * FROM teachers WHERE salary = (SELECT MAX(salary) FROM teachers);',
        'SELECT * FROM teachers WHERE salary = (SELECT ROUND(AVG(salary)) FROM teachers);',
        'SELECT * FROM students WHERE credits = (SELECT MAX(credits) FROM students) LIMIT 200;',
        'SELECT * FROM students WHERE credits = (SELECT ROUND(AVG(credits)) FROM students) LIMIT 200;'
    ]
    then = time.time()
    for query in queries:
        cursor.execute(query)
        cursor.fetchall()
    total_time = time.time() - then
    print(f'Derived queries: {total_time:.2f} seconds')
    test_results['derived_queries'] = total_time
    connection.close()

def integer_sort():
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    queries = [
        'SELECT * FROM students ORDER BY credits DESC LIMIT 1000;',
        'SELECT * FROM teachers ORDER BY salary DESC LIMIT 1000;'
    ]
    then = time.time()
    for query in queries:
        cursor.execute(query)
        cursor.fetchall()
    total_time = time.time() - then
    print(f'Table sort integer: {total_time:.2f} seconds')
    test_results['integer_sort'] = total_time
    connection.close()

def string_sort():
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    queries = [
        'SELECT * FROM students ORDER BY first_name DESC LIMIT 1000;',
        'SELECT * FROM students ORDER BY last_name ASC LIMIT 1000;',
        'SELECT * FROM teachers ORDER BY last_name DESC LIMIT 1000;',
        'SELECT * FROM teachers ORDER BY first_name ASC LIMIT 1000;'
    ]
    then = time.time()
    for query in queries:
        cursor.execute(query)
        cursor.fetchall()
    total_time = time.time() - then
    print(f'Table sort string: {total_time:.2f} seconds')
    test_results['string_sort'] = total_time
    connection.close()

def mass_update():
    global female_names
    global male_names
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    random_male_name = random.choice(male_names)
    random_female_name = random.choice(female_names)
    queries = [
        f'UPDATE students SET first_name = "Andriw" WHERE first_name = "{random_male_name}"',
        f'UPDATE teachers SET first_name = "{random_female_name}" WHERE first_name = "Ariadny"'
       ]
    then = time.time()
    for query in queries:
        cursor.execute(query)
        connection.commit()
    total_time = time.time() - then
    print(f'Update statement: {total_time:.2f} seconds')
    test_results['update'] = total_time
    connection.close()

def math_operations():
    global test_results
    connection = pool.get_connection()
    cursor = connection.cursor()
    queries = [
        'SELECT SQRT(credits) FROM students ORDER BY credits DESC LIMIT 1500;',
        'SELECT EXP(credits) FROM students ORDER BY credits DESC LIMIT 1500;',
        'SELECT SIN(credits) FROM students ORDER BY credits DESC LIMIT 1500;',
        'SELECT COS(credits) FROM students ORDER BY credits DESC LIMIT 1500;',
        'SELECT LOG(credits) FROM students ORDER BY credits DESC LIMIT 1500;',
        'SELECT POW(credits, 3) FROM students ORDER BY credits DESC LIMIT 1500;'
    ]
    then = time.time()
    for query in queries:
        cursor.execute(query)
        cursor.fetchall()
    total_time = time.time() - then
    print(f'Math operations: {total_time:.2f} seconds')
    test_results['math_operations'] = total_time
    connection.close()

def main():
    offset()
    index_lookup()
    joined_index_lookup()
    string_lookup()
    regex_lookup()
    derived_queries()
    integer_sort()
    string_sort()
    mass_update()
    math_operations()
    parameter_variables()

if __name__ == '__main__':
    main()
