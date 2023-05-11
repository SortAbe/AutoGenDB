CREATE DATABASE University;

USE University;

CREATE TABLE department(
	dept_name VARCHAR(80) NOT NULL,
	college VARCHAR(80),
	building INT,
	PRIMARY KEY(dept_name)
);

CREATE TABLE student(
	ID INT NOT NULL AUTO_INCREMENT,
	firstName VARCHAR(20) NOT NULL,
	lastName VARCHAR(20) NOT NULL,
	gender BOOLEAN NOT NULL,
	dept_name VARCHAR(80) NOT NULL,
	credits INT,
	PRIMARY KEY(ID),
	FOREIGN KEY(dept_name) REFERENCES department(dept_name)
);

CREATE TABLE instructor(
	ID INT NOT NULL AUTO_INCREMENT,
	firstName VARCHAR(20) NOT NULL,
	lastName VARCHAR(20) NOT NULL,
	gender BOOLEAN NOT NULL,
	dept_name VARCHAR(80) NOT NULL,
	PRIMARY KEY(ID),
	FOREIGN KEY(dept_name) REFERENCES department(dept_name)
);

CREATE TABLE course(
	course_id INT NOT NULL,
	title VARCHAR(20),
	dept_name VARCHAR(80) NOT NULL,
	credits INT,
	PRIMARY KEY(course_id),
	FOREIGN KEY(dept_name) REFERENCES department(dept_name)
);

CREATE TABLE section(
	course_id INT NOT NULL,
	sec_id INT NOT NULL,
	semester VARCHAR(8) NOT NULL,
	year YEAR NOT NULL,
	building VARCHAR(3),
	room_no INT,
	PRIMARY KEY(course_id, sec_id, semester, year),
	FOREIGN KEY(course_id) REFERENCES course(course_id)
);

CREATE TABLE classroom(
	building VARCHAR(3) NOT NULL,
	room_no INT NOT NULL,
	cpacity INT,
	PRIMARY KEY(building, room_no)
);

CREATE TABLE teaches(
	ID INT NOT NULL, 
	course_id INT NOT NULL,
	sec_id INT NOT NULL,
	semester VARCHAR(8) NOT NULL,
	year YEAR NOT NULL,
	PRIMARY KEY(ID, course_id, sec_id, semester, year),
	FOREIGN KEY(ID) REFERENCES instructor(ID),
	FOREIGN KEY(course_id) REFERENCES course(course_id),
	FOREIGN KEY(course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year)
);

CREATE TABLE takes(
	ID INT NOT NULL,
	course_id INT NOT NULL,
	sec_id INT NOT NULL,
	semester VARCHAR(8) NOT NULL,
	year YEAR NOT NULL,
	grade VARCHAR(2),
	PRIMARY KEY(ID, course_id, sec_id, semester, year),
	FOREIGN KEY(ID) REFERENCES student(ID),
	FOREIGN KEY(course_id) REFERENCES course(course_id),
	FOREIGN KEY(course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year)
);
