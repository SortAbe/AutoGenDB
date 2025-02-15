#!/bin/env python3.11
# Abrahan Diaz
# Version 2.4

import datetime
import time
import random
from mysql.connector import pooling
from mysql.connector import errors
from concurrent.futures import ThreadPoolExecutor

class Generator:

    pool = pooling.MySQLConnectionPool(
        pool_name='pool',
        pool_size=32,
        user='py',
        host='localhost',
        database='University',
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

    def __init__(self):
        connector = self.pool.get_connection()
        cursor = connector.cursor()

        cursor.execute('SELECT * FROM department')
        results = cursor.fetchall()
        if not results:
            print('Failed to retrieve table department!')
            exit(1)
        for row in results:
            self.department_list.append(row[0])

        cursor.execute('SELECT * FROM course')
        results = cursor.fetchall()
        if not results:
            print('Failed to retrieve tables course!')
            exit(1)
        for row in results:
            self.course_list.append(row)

        cursor.execute('SELECT * FROM addresses')
        results = cursor.fetchall()
        if not results:
            print('Failed to retrieve table addresses!')
            exit(1)
        for row in results:
            self.address_list.append(row)

        cursor.execute('SELECT * FROM femaleNames')
        results = cursor.fetchall()
        if not results:
            print('Failed to retrieve table femaleNames!')
            exit(1)
        for row in results:
            self.female_names.append(row[0])

        cursor.execute('SELECT * FROM maleNames')
        results = cursor.fetchall()
        if not results:
            print('Failed to retrieve table maleNames!')
            exit(1)
        for row in results:
            self.male_names.append(row[0])

        cursor.execute('SELECT * FROM lastNames')
        results = cursor.fetchall()
        if not results:
            print('Failed to retrieve table lastNames!')
            exit(1)
        for row in results:
            self.last_names.append(row[0])

        connector.close()

    def generate_students(self, thread_id, rows=100_000):
        connector = self.pool.get_connection()
        cursor = connector.cursor()

        sql = 'INSERT INTO student (ID, firstName, lastName, gender,\
            dept_name, registered, credits)\
            VALUES (%s, %s, %s, %s, %s, %s, %s);'

        sql2 = 'INSERT INTO sAddress (ID, addr1, addr2, city, state, zip)\
            VALUES (%s, %s, %s, %s, %s, %s);'

        sql3 = 'INSERT INTO sContact (ID, email, phone) VALUES (%s, %s, %s);'

        key_date = datetime.date(2015, 1, 1)
        offset = thread_id * rows
        data_batch1 = []
        data_batch2 = []
        data_batch3 = []
        for row in range(rows):
            if random.getrandbits(1):
                gender = 'Male'
                first = random.choice(self.male_names)
            else:
                gender = 'Female'
                first = random.choice(self.female_names)
            last = random.choice(self.last_names)
            date_delta = key_date + datetime.timedelta(
                days=random.choice(range(3600))
            )
            data = (
                row + offset, #ID
                first,
                last,
                gender,
                random.choice(self.department_list), #dept_name
                date_delta.strftime('%Y-%m-%d'), #registered
                random.randint(0,120), #credits
            )

            addr = random.choice(self.address_list)
            data2 = (
                row + offset, #ID
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

    def generate_teachers(self, thread_id, rows=10_000):
        connector = self.pool.get_connection()
        cursor = connector.cursor()

        sql = 'INSERT INTO instructor \
            (ID, firstName, lastName, gender, dept_name, salary) \
            VALUES (%s, %s, %s, %s, %s, %s);'

        sql2 = 'INSERT INTO tAddress (ID, addr1, addr2, city, state, zip) \
            VALUES (%s, %s, %s, %s, %s, %s);'

        sql3 = 'INSERT INTO tContact (ID, email, phone) VALUES (%s, %s, %s);'

        offset = thread_id * rows
        data_batch1 = []
        data_batch2 = []
        data_batch3 = []
        for row in range(rows):
            if random.getrandbits(1):
                gender = 'Male'
                first = random.choice(self.male_names)
            else:
                gender = 'Female'
                first = random.choice(self.female_names)

            last = random.choice(self.last_names)
            data = (
                row + offset, #ID
                first,
                last,
                gender,
                random.choice(self.department_list), #dept_name
                random.choice(range(80_000, 160_000)), #salary
            )

            addr = random.choice(self.address_list)
            data2 = (
                    row + offset, #ID
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

    def generate_classes(self, thread_id, rows=10_000):
        connector = self.pool.get_connection()
        cursor = connector.cursor()
        cursor.execute(
            'SELECT course.course_id, department.building\
            FROM course JOIN department ON course.dept_name = department.dept_name;'
        )
        results = cursor.fetchall()
        sql = 'INSERT INTO class (class_id, course_id, semester, year, building, room_no, capacity)\
            VALUES(%s, %s, %s, %s, %s, %s, %s);'

        offset = thread_id * rows
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

    def generate_takes(self, thread_id, rows=100_000):
        connector = self.pool.get_connection()
        cursor = connector.cursor()
        cursor.execute('SELECT MAX(ID) FROM student')
        student_max = cursor.fetchone()[0]
        cursor.execute('SELECT MIN(class_id) FROM class')
        class_min = cursor.fetchone()[0]
        cursor.execute('SELECT MAX(class_id) FROM class')
        class_max = cursor.fetchone()[0]

        sql = 'INSERT INTO takes(ID, class_id, grade)\
            VALUES(%s, %s, %s)'

        offset = thread_id * rows
        data_batch = []
        for row in range(rows):
            if (row + offset) > student_max:
                break
            class_list = []
            for _ in range(3):
                class_id = random.randint(class_min, class_max)
                while class_id in class_list:
                    class_id = random.randint(class_min, class_max)
                class_list.append(class_id)
                data = (
                    row + offset, #ID
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

    def generate_teaches(self, thread_id, rows=10_000):
        connector = self.pool.get_connection()
        cursor = connector.cursor()
        cursor.execute('SELECT MAX(ID) FROM instructor')
        student_max = cursor.fetchone()[0]
        cursor.execute('SELECT MIN(class_id) FROM class')
        class_min = cursor.fetchone()[0]
        cursor.execute('SELECT MAX(class_id) FROM class')
        class_max = cursor.fetchone()[0]

        sql = 'INSERT INTO teaches(ID, class_id)\
            VALUES(%s, %s)'

        offset = thread_id * rows
        data_batch = []
        for row in range(rows):
            if (row + offset) > student_max:
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


if __name__ == '__main__':
    generator = Generator()
    then = time.time()
    with ThreadPoolExecutor(max_workers=32) as executor:
        for thread in range(32):
            executor.submit(generator.generate_students, thread, 200_000)
            executor.submit(generator.generate_teachers, thread, 20_000)
            executor.submit(generator.generate_classes, thread, 20_000)
    print(f'Stage one time: {time.time() - then:.2f} seconds')
    then = time.time()
    with ThreadPoolExecutor(max_workers=32) as executor:
        for thread in range(32):
            executor.submit(generator.generate_takes, thread, 200_000)
            executor.submit(generator.generate_teaches, thread, 20_000)
    print(f'Stage two time: {time.time() - then:.2f} seconds')
