#!/bin/env python3
#Abrahan Diaz
#Version 0.8


import random
import re
import time
import mysql.connector

class Filler:
	cnx = mysql.connector.connect(
		host='localhost',
		user='py',
		password='password123!',
		database='University',
		port=7707
	)
	cursor = cnx.cursor()
	departmentList = []
	femaleNames = []
	maleNames = []
	lastNames = []

	def __init__(self):
		#get deparments
		query = 'SELECT * FROM department'
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		for row in results:
			self.departmentList.append(row[0])
		#get names
		with open('female.names', 'r') as femf:
			lines = femf.readlines()
			for line in lines:
				self.femaleNames.append(line)
		with open('male.names', 'r') as malf:
			lines = malf.readlines()
			for line in lines:
				self.maleNames.append(line)
		with open('last.names', 'r') as lasf:
			lines = lasf.readlines()
			for line in lines:
				self.lastNames.append(line)

	def fillFemales(self, rows=1000):
		flen = len(self.femaleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.femaleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO student (firstName, lastName, gender, dept_name, credits) VALUES (%s, %s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.femaleNames[i%flen], self.lastNames[i%llen], True, self.departmentList[i%dlen] , credit)
			self.cursor.execute(sql, data)
		self.cnx.commit()
		
	def fillFemalesT(self, rows=100):
		flen = len(self.femaleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.femaleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO instructor (firstName, lastName, gender, dept_name) VALUES (%s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.femaleNames[i%flen], self.lastNames[i%llen], True, self.departmentList[i%dlen])
			self.cursor.execute(sql, data)
		self.cnx.commit()

	def fillMales(self, rows=1000):
		mlen = len(self.maleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.maleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO student (firstName, lastName, gender, dept_name, credits) VALUES (%s, %s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.maleNames[i%mlen], self.lastNames[i%llen], False, self.departmentList[i%dlen] , credit)
			self.cursor.execute(sql, data)
		self.cnx.commit()
	
	def fillMalesT(self, rows=100):
		mlen = len(self.maleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.maleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO instructor (firstName, lastName, gender, dept_name) VALUES (%s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.maleNames[i%mlen], self.lastNames[i%llen], False, self.departmentList[i%dlen])
			self.cursor.execute(sql, data)
		self.cnx.commit()

	def close(self):
		self.cursor.close()
		self.cnx.close()


if '__NAME__' == '__NAME__':
	filler = Filler()
	filler.fillFemales()
	filler.fillMales()
	filler.fillFemalesT()
	filler.fillMalesT()
	filler.close()
