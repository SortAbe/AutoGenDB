#!/bin/env python3
#Abrahan Diaz
#Version 1.1 Staging version

import random
import mysql.connector
from random_address import real_random_address as rra
import json
import datetime
import time
import os
import sys

class Filler:

	cnx = mysql.connector.connect(
		host=os.environ.get('server'),
		user='py',
		password=os.environ.get('dbpass'),
		database='University',
		port=7707
	)
	cursor = cnx.cursor()
	departmentList = []
	femaleNames = []
	maleNames = []
	lastNames = []
	areaCode = {}

	def __init__(self):
		#get deparments
		query = 'SELECT * FROM department'
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		for row in results:
			self.departmentList.append(row[0])
		#get names
		with open('./lists/female.names', 'r') as femf:
			lines = femf.readlines()
			for line in lines:
				self.femaleNames.append(line)
		with open('./lists/male.names', 'r') as malf:
			lines = malf.readlines()
			for line in lines:
				self.maleNames.append(line)
		with open('./lists/last.names', 'r') as lasf:
			lines = lasf.readlines()
			for line in lines:
				self.lastNames.append(line)
		#area code file for phone numbers
		with open('./lists/areac.json', 'r') as jsonf:
			data = jsonf.read()
			self.areaCode = json.loads(data)

	def fill_student(self, offset, gen=True, rows=100_000):
		gender = gen
		if gen:
			flen = len(self.femaleNames)
			random.shuffle(self.femaleNames)
		else:
			flen = len(self.maleNames)
			random.shuffle(self.maleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.lastNames)
		key_date = datetime.date(2015, 1, 1)
		random.shuffle(self.departmentList)

		sql = "INSERT INTO student (ID, firstName, lastName, gender, \
			dept_name, registered, credits) \
			VALUES (%s, %s, %s, %s, %s, %s, %s);"

		sql2 = "INSERT INTO sAddress (ID, addr1, addr2, city, state, zip) \
			VALUES (%s, %s, %s, %s, %s, %s);"

		sql3 = "INSERT INTO sContact (ID, email, phone) VALUES (%s, %s, %s);"

		count = 0 + offset
		for i in range(rows):
			credit = random.choice(range(60))	
			date_delta = key_date + datetime.timedelta(days=random.choice(range(3600)))
			if gender:
				first = self.femaleNames[i%flen].strip()
			else:
				first = self.maleNames[i%flen].strip()
			last = self.lastNames[i%llen].strip()

			data = (count, first, last, gender, self.departmentList[i%dlen].strip(), date_delta.strftime('%Y-%m-%d'), credit)

			addr = rra()
			if 'city' not in addr:
				addr['city'] = ''

			data2 = (count, addr['address1'], addr['address2'], addr['city'], addr['state'], addr['postalCode'])

			data3 = (count, (first.lower() + last.lower() + addr['postalCode'] + '@sqlu.edu'), 
			( '(' + random.choice(self.areaCode[addr['state']]) + ')-'\
			+ str(random.choice(range(1000,2000)))[1:] + '-' + str(random.choice(range(10000,20000)))[1:]))

			self.cursor.execute(sql, data)
			self.cursor.execute(sql2, data2)
			self.cursor.execute(sql3, data3)
			count += 1
			if count% 1000 == 0:
				self.cnx.commit()
			if count == 100_000 + offset:
				return
		self.cnx.commit()
		
	def fill_instructor(self, offset, rows=10_000, gen=True):
		gender = gen
		if gen:
			flen = len(self.femaleNames)
			random.shuffle(self.femaleNames)
		else:
			flen = len(self.maleNames)
			random.shuffle(self.maleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		
		sql = "INSERT INTO instructor \
			(ID, firstName, lastName, gender, dept_name, salary) \
			VALUES (%s, %s, %s, %s, %s, %s);"

		sql2 = "INSERT INTO tAddress (ID, addr1, addr2, city, state, zip) \
			VALUES (%s, %s, %s, %s, %s, %s);"

		sql3 = "INSERT INTO tContact (ID, email, phone) VALUES (%s, %s, %s);"

		count = 0 + offset
		for i in range(rows):
			if gender:
				first = self.femaleNames[i%flen].strip()
			else:
				first = self.maleNames[i%flen].strip()
			last = self.lastNames[i%llen].strip()
			salary = random.choice(range(80_000,160_000))

			data = (count, first, last, gender, self.departmentList[i%dlen].strip(), salary)

			addr = rra()
			if 'city' not in addr:
				addr['city'] = ''

			data2 = (count, addr['address1'], addr['address2'], addr['city'], addr['state'], addr['postalCode'])

			data3 = (count, (first.lower() + last.lower() + addr['postalCode'] + '@teacher.sqlu.edu'), 
				( '(' + random.choice(self.areaCode[addr['state']]) \
				+ ')-' + str(random.choice(range(1000,2000)))[1:] + '-' + str(random.choice(range(10000,20000)))[1:]))

			self.cursor.execute(sql, data)
			self.cursor.execute(sql2, data2)
			self.cursor.execute(sql3, data3)
			count += 1
			if count% 1000 == 0:
				self.cnx.commit()
			if count == 10_000 + offset:
				return
		self.cnx.commit()

	def class_(self, offset, year=2023, semester='Spring'):
		self.cursor.execute(
			'SELECT course.course_id, course.dept_name, department.building\
			 FROM course JOIN department ON course.dept_name = department.dept_name\
			 ORDER BY department.building;')
		view = self.cursor.fetchall()
		building = None
		room_no = 0

		sql = 'INSERT INTO class (class_id, course_id, semester, year, building, room_no) \
			VALUES(%s, %s, %s, %s, %s, %s);'

		sql2 = 'INSERT IGNORE INTO classroom \
			(building, room_no, capacity) VALUES(%s, %s, %s);'

		count = 0 + offset
		for row in view:
			if row[2] != building:
				room_no = 0
				building = row[2]
			for _ in range(random.choice(range(6))):
				data = (count, row[0], semester, year, building, room_no)
				room_no += 1
				data2 = (building, room_no, random.choice(range(6, 11)) * 10)
				self.cursor.execute(sql, data)
				self.cursor.execute(sql2, data2)
				count += 1
				if count % 1000 == 0:
					self.cnx.commit()
				if count == 30_000 + offset:
					self.cnx.commit()
					return

	def teaches(self, offset):
		self.cursor.execute('SELECT dept_name FROM department LIMIT 1 OFFSET ' + str(offset) + ';')
		for dept in self.cursor.fetchall():
			self.cursor.execute('SELECT ID FROM instructor WHERE dept_name = \"' + dept[0] + '\";')
			teachers = self.cursor.fetchall()
			teachNums = len(teachers)
			teachSelect = 0
			self.cursor.execute('SELECT course_id FROM course WHERE dept_name = \"' + dept[0] + '\";')
			count = 0
			for course in self.cursor.fetchall():
				self.cursor.execute('SELECT class_id FROM class WHERE course_id = \"' + str(course[0]) + '\";')
				for class_ in self.cursor.fetchall():

					sql = 'INSERT IGNORE INTO teaches (ID, course_id, class_id) VALUES (%s, %s, %s);'

					data = (str(teachers[teachSelect % teachNums][0]), str(course[0]), str(class_[0])) 
					self.cursor.execute(sql, data)
					teachSelect += 1
					count += 1
					if count % 1000 == 0:
						self.cnx.commit()
		self.cnx.commit()

	def takes(self, offset):
		self.cursor.execute('SELECT dept_name FROM department LIMIT 1 OFFSET ' + str(offset) + ';')
		count = 0
		for dept in self.cursor.fetchall():
			self.cursor.execute(
			'SELECT course.course_id, class.class_id, class.building, class.room_no\
			 FROM course JOIN class ON course.course_id = class.course_id\
			 WHERE course.dept_name LIKE \"' + dept[0]+ '\";')
			classes =  self.cursor.fetchall()
			self.cursor.execute('SELECT ID FROM student WHERE dept_name = \"' + dept[0] + '\";')
			for student in self.cursor.fetchall():

				sql = 'INSERT IGNORE INTO takes (ID, course_id, class_id) VALUES (%s, %s, %s);'

				for _ in range(random.choice(range(6))):
					try:
						choice = random.choice(classes)
					except:
						continue
					data = (str(student[0]), str(choice[0]), str(choice[1]))
					self.cursor.execute(sql, data)
					count += 1
					if count % 1000 == 0:
						self.cnx.commit()
					if count == 30_000:
						return
			self.cnx.commit()

	def close(self):
		self.cursor.close()
		self.cnx.close()


if __name__ == '__main__':
	filler = Filler()
	id = int(sys.argv[1])
	even = False
	gender = True
	if id % 2 == 0:
		gender = False
		even = True
	thrOffset = int(sys.argv[2])
	start = time.time()
	time.sleep(random.randint(0, 60))
	if even:
		while time.time() - start < 3600 * 2:
			filler.fill_student(id * 100_000, gender)
			filler.fill_instructor(id * 10_000)
			filler.class_(id * 30_000)
			id += thrOffset
			gender = not gender
	else:
		while time.time() - start < 3600 * 2:
			filler.class_(id * 30_000)
			filler.fill_instructor(id * 10_000)
			filler.fill_student(id * 100_000, gender)
			id += thrOffset
			gender = not gender
	if id < 54:
		filler.teaches(id)
		filler.takes(id)
	filler.close()
