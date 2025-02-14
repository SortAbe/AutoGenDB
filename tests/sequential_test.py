#!/usr/bin/env python3.11

import os
import random
import time

from mysql import connector

connection = connector.connect(
    user='py',
    host='localhost',
    database='University',
    password=os.environ.get('dbpass'),
    port='3306',
    connect_timeout=3600,
)
cursor = connection.cursor()

then = time.time()
for _ in range(5000):
    cursor.execute(
        f'SELECT * FROM student WHERE ID = {random.randint(0, 1_600_000)};'
    )
    cursor.fetchone()
for _ in range(5000):
    cursor.execute(
        f'SELECT * FROM sContact WHERE ID = {random.randint(0, 1_600_000)};'
    )
    cursor.fetchone()
for _ in range(5000):
    cursor.execute(
        f'SELECT * FROM sAddress WHERE ID = {random.randint(0, 1_600_000)};'
    )
    cursor.fetchone()
for _ in range(500):
    cursor.execute(
        f'SELECT * FROM instructor WHERE ID = {random.randint(0, 160_000)};'
    )
    cursor.fetchone()
for _ in range(500):
    cursor.execute(
        f'SELECT * FROM tContact WHERE ID = {random.randint(0, 160_000)};'
    )
    cursor.fetchone()
for _ in range(500):
    cursor.execute(
        f'SELECT * FROM tAddress WHERE ID = {random.randint(0, 160_000)};'
    )
    cursor.fetchone()
print(f'Simple integer index seq: {time.time() - then:.2f} seconds')
