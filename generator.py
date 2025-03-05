#!/bin/env python3.11
# Abrahan Diaz
# Version 2.5

import datetime
import time
import random
from mysql.connector import pooling, errors
from concurrent.futures import ThreadPoolExecutor

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
students_max: int
teachers_max: int
classes_max: int
connector = pool.get_connection()
cursor = connector.cursor()

def offset():
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global students_max
    global teachers_max
    global classes_max
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
        cursor.execute('SELECT COUNT(*) FROM students')
        if cursor.fetchone()[0] == 0:
            students_max = 0
        else:
            print('Failed to retrieve students max!')
            exit(1)
    else:
        students_max = result

    cursor.execute('SELECT MAX(id) FROM teachers')
    result = cursor.fetchone()[0]
    if not result:
        cursor.execute('SELECT COUNT(*) FROM teachers')
        if cursor.fetchone()[0] == 0:
            teachers_max = 0
        else:
            print('Failed to retrieve teachers max!')
            exit(1)
    else:
        teachers_max = result

    cursor.execute('SELECT MAX(class_id) FROM classes')
    result = cursor.fetchone()[0]
    if not result:
        cursor.execute('SELECT COUNT(*) FROM classes')
        if cursor.fetchone()[0] == 0:
            classes_max = 0
        else:
            print('Failed to retrieve classes max!')
            exit(1)
    else:
        classes_max = result
    connector.close()

def generate_students(thread_id, rows=100_000):
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global students_max
    connector = pool.get_connection()
    cursor = connector.cursor()

    sql = 'INSERT INTO students (id, first_name, last_name, gender,\
        dept_name, registered, credits)\
        VALUES (%s, %s, %s, %s, %s, %s, %s);'

    sql2 = 'INSERT INTO students_address (id, addr1, addr2, city, state, zip)\
        VALUES (%s, %s, %s, %s, %s, %s);'

    sql3 = 'INSERT INTO students_contact (id, email, phone) VALUES (%s, %s, %s);'

    key_date = datetime.date(2015, 1, 1)
    offset = thread_id * rows + students_max + 1
    data_batch1 = []
    data_batch2 = []
    data_batch3 = []
    for row in range(rows):
        if random.getrandbits(1):
            gender = 'Male'
            first = random.choice(male_names)
        else:
            gender = 'Female'
            first = random.choice(female_names)
        last = random.choice(last_names)
        date_delta = key_date + datetime.timedelta(
            days=random.choice(range(3600))
        )
        data = (
            row + offset, #id
            first,
            last,
            gender,
            random.choice(department_list), #dept_name
            date_delta.strftime('%Y-%m-%d'), #registered
            random.randint(0,120), #credits
        )

        addr = random.choice(address_list)
        data2 = (
            row + offset, #id
            str(random.randint(0,1000)) + ' ' + addr[0], #addr1
            random.choice(['', '#', 'Apt ', 'Appartment ']) + str(random.randint(1,1000)), #addr2
            addr[1], #city
            addr[2], #state
            addr[3] #zip
        )

        data3 = (
            row + offset, #id
            (first.lower() + last.lower() + str(random.randint(1,1000)) + '@sqlu.edu'), #email
            (
                '('
                  + str(addr[3])[0:3]
                + ')-'
                + str(random.choice(range(1000, 2000)))[1:]
                + '-'
                + str(random.choice(range(10000, 20000)))[1:]
            ), #phone
        )
        data_batch1.append(data)
        data_batch2.append(data2)
        data_batch3.append(data3)
        if row % 1000 == 0 and row != 0:
            try:
                cursor.executemany(sql, data_batch1)
                cursor.executemany(sql2, data_batch2)
                cursor.executemany(sql3, data_batch3)
                connector.commit()
                data_batch1.clear()
                data_batch2.clear()
                data_batch3.clear()
            except errors.DatabaseError as e:
                print(e)
    try:
        cursor.executemany(sql, data_batch1)
        cursor.executemany(sql2, data_batch2)
        cursor.executemany(sql3, data_batch3)
        connector.commit()
        data_batch1.clear()
        data_batch2.clear()
        data_batch3.clear()
    except errors.DatabaseError as e:
        print(e)
    connector.close()

def generate_teachers(thread_id, rows=10_000):
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global teachers_max
    connector = pool.get_connection()
    cursor = connector.cursor()

    sql = 'INSERT INTO teachers \
        (ID, first_name, last_name, gender, dept_name, salary) \
        VALUES (%s, %s, %s, %s, %s, %s);'

    sql2 = 'INSERT INTO teachers_address (id, addr1, addr2, city, state, zip) \
        VALUES (%s, %s, %s, %s, %s, %s);'

    sql3 = 'INSERT INTO teachers_contact (id, email, phone) VALUES (%s, %s, %s);'

    offset = thread_id * rows + teachers_max + 1
    data_batch1 = []
    data_batch2 = []
    data_batch3 = []
    for row in range(rows):
        if random.getrandbits(1):
            gender = 'Male'
            first = random.choice(male_names)
        else:
            gender = 'Female'
            first = random.choice(female_names)

        last = random.choice(last_names)
        data = (
            row + offset, #id
            first,
            last,
            gender,
            random.choice(department_list), #dept_name
            random.choice(range(80_000, 160_000)), #salary
        )

        addr = random.choice(address_list)
        data2 = (
                row + offset, #id
                str(random.randint(0,1000)) + ' ' + addr[0], #addr1
                random.choice(['', '#', 'Apt ', 'Appartment ']) + str(random.randint(1,1000)), #addr2
                addr[1], #city
                addr[2], #state
                addr[3] #zip
                )

        data3 = (
            row + offset, #ID
            (first.lower() + last.lower() + str(random.randint(1,1000)) + '@sqlu.edu'), #email
            (
                '('
                + str(addr[3])[0:3]
                + ')-'
                + str(random.choice(range(1000, 2000)))[1:]
                + '-'
                + str(random.choice(range(10000, 20000)))[1:]
            ), #phone
        )
        data_batch1.append(data)
        data_batch2.append(data2)
        data_batch3.append(data3)
        if row % 1000 == 0 and row != 0:
            try:
                cursor.executemany(sql, data_batch1)
                cursor.executemany(sql2, data_batch2)
                cursor.executemany(sql3, data_batch3)
                connector.commit()
                data_batch1.clear()
                data_batch2.clear()
                data_batch3.clear()
            except errors.DatabaseError as e:
                print(e)
    try:
        cursor.executemany(sql, data_batch1)
        cursor.executemany(sql2, data_batch2)
        cursor.executemany(sql3, data_batch3)
        connector.commit()
        data_batch1.clear()
        data_batch2.clear()
        data_batch3.clear()
    except errors.DatabaseError as e:
        print(e)
    connector.close()

def generate_classes(thread_id, rows=10_000):
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global classes_max
    connector = pool.get_connection()
    cursor = connector.cursor()
    cursor.execute(
        'SELECT courses.course_id, departments.building\
        FROM courses JOIN departments ON courses.dept_name = departments.dept_name;'
    )
    results = cursor.fetchall()
    sql = 'INSERT INTO classes (class_id, course_id, semester, year, building, room_no, capacity)\
        VALUES(%s, %s, %s, %s, %s, %s, %s);'

    offset = thread_id * rows + classes_max + 1
    data_batch = []
    for row in range(rows):
        course = random.choice(results)
        data = (
            row + offset, #class_id
            course[0], #course_id
            random.choice(['Spring', 'Summer', 'Fall', 'Winter']), #semester
            random.randint(2015, 2025), #year
            course[1], #building
            random.randint(1, 200), #room_no
            random.randint(8, 30), #capacity
        )
        data_batch.append(data)
        if row % 1000 == 0:
            try:
                cursor.executemany(sql, data_batch)
                connector.commit()
                data_batch.clear()
            except errors.DatabaseError as e:
                print(e)
    try:
        cursor.executemany(sql, data_batch)
        connector.commit()
        data_batch.clear()
    except errors.DatabaseError as e:
        print(e)
    connector.close()

def generate_takes(thread_id, rows=100_000):
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global students_max
    global classes_max
    connector = pool.get_connection()
    cursor = connector.cursor()
    cursor.execute('SELECT MAX(id) FROM students')
    students_new_max = cursor.fetchone()[0]
    class_min = classes_max + 1
    cursor.execute('SELECT MAX(class_id) FROM classes')
    class_max = cursor.fetchone()[0]

    sql = 'INSERT INTO takes(id, class_id, grade)\
        VALUES(%s, %s, %s)'

    offset = thread_id * rows + students_max + 1
    data_batch = []
    for row in range(rows):
        if (row + offset) > students_new_max:
            break
        class_list = []
        for _ in range(3):
            class_id = random.randint(class_min, class_max)
            while class_id in class_list:
                class_id = random.randint(class_min, class_max)
            class_list.append(class_id)
            data = (
                row + offset, #id
                class_id, #class_id
                random.choice(['A', 'B', 'C', 'D', 'F']) + random.choice(['+', '-', '']) #grade
            )
            data_batch.append(data)
        class_list.clear()
        if row % 1000 == 0:
            try:
                cursor.executemany(sql, data_batch)
                connector.commit()
                data_batch.clear()
            except errors.DatabaseError as e:
                print(e)
    try:
        cursor.executemany(sql, data_batch)
        connector.commit()
        data_batch.clear()
    except errors.DatabaseError as e:
        print(e)
    connector.close()

def generate_teaches(thread_id, rows=10_000):
    global department_list
    global course_list
    global address_list
    global female_names
    global male_names
    global last_names
    global teachers_max
    global classes_max
    connector = pool.get_connection()
    cursor = connector.cursor()
    cursor.execute('SELECT MAX(id) FROM teachers')
    teachers_new_max = cursor.fetchone()[0]
    class_min = classes_max + 1
    cursor.execute('SELECT MAX(class_id) FROM classes')
    class_max = cursor.fetchone()[0]

    sql = 'INSERT INTO teaches(id, class_id)\
        VALUES(%s, %s)'

    offset = thread_id * rows + teachers_max + 1
    data_batch = []
    for row in range(rows):
        if (row + offset) > teachers_new_max:
            break
        data = (
            row + offset, #ID
            random.randint(class_min, class_max), #class_id
        )
        data_batch.append(data)
        if row % 1000 == 0:
            try:
                cursor.executemany(sql, data_batch)
                connector.commit()
                data_batch.clear()
            except errors.DatabaseError as e:
                print(e)
    try:
        cursor.executemany(sql, data_batch)
        connector.commit()
        data_batch.clear()
    except errors.DatabaseError as e:
        print(e)
    connector.close()

def main(threads=16, data=1) -> None:
    """
    This functions starts the program.
    Parameters:
        threads (int): Number of threads
        data (int): Amount of data to add in GB
    Returns:
        None: nothing is returned
    """
    offset()
    then = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for thread in range(threads):
            executor.submit(generate_students, thread, data * 110_000)
            executor.submit(generate_teachers, thread, data * 11_000)
            executor.submit(generate_classes, thread, data * 11_000)
    print(f'Stage one time: {time.time() - then:.2f} seconds')
    then = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for thread in range(threads):
            executor.submit(generate_takes, thread, data * 110_000)
            executor.submit(generate_teaches, thread, data * 11_000)
    print(f'Stage two time: {time.time() - then:.2f} seconds')

if __name__ == '__main__':
    main()
