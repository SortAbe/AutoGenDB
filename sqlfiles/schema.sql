CREATE DATABASE university;

USE university;

CREATE TABLE departments (
  dept_name VARCHAR(80) NOT NULL,
  college VARCHAR(80),
  building INT,
  PRIMARY KEY (dept_name)
);

CREATE TABLE students (
  id INT NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  gender ENUM('Male', 'Female'),
  dept_name VARCHAR(80) NOT NULL,
  registered DATE NOT NULL,
  credits INT,
  PRIMARY KEY (id),
  FOREIGN KEY (dept_name) REFERENCES departments (dept_name)
);

CREATE TABLE students_address (
  id INT NOT NULL,
  addr1 VARCHAR(100),
  addr2 VARCHAR(100),
  city VARCHAR(100),
  state VARCHAR(10),
  zip INT,
  PRIMARY KEY (ID),
  FOREIGN KEY (ID) REFERENCES students (id)
);

CREATE TABLE students_contact (
  id INT NOT NULL,
  email varchar(50),
  phone varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES students (id)
);

CREATE TABLE teachers (
  id INT NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  gender ENUM('Male', 'Female'),
  dept_name VARCHAR(80) NOT NULL,
  salary INT,
  PRIMARY KEY (id),
  FOREIGN KEY (dept_name) REFERENCES departments (dept_name)
);

CREATE TABLE teachers_address (
  ID INT NOT NULL,
  addr1 VARCHAR(100),
  addr2 VARCHAR(100),
  city VARCHAR(100),
  state VARCHAR(10),
  zip INT,
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES teachers (id)
);

CREATE TABLE teachers_contact (
  id INT NOT NULL,
  email varchar(50),
  phone varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES teachers (id)
);

CREATE TABLE courses (
  course_id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(80),
  dept_name VARCHAR(80) NOT NULL,
  credits INT,
  PRIMARY KEY (course_id),
  FOREIGN KEY (dept_name) REFERENCES departments (dept_name)
);

CREATE TABLE classes (
  class_id INT NOT NULL,
  course_id INT NOT NULL,
  semester VARCHAR(8) NOT NULL,
  year YEAR NOT NULL,
  building INT,
  room_no INT,
  capacity INT,
  PRIMARY KEY (class_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

CREATE TABLE takes (
  id INT NOT NULL,
  class_id INT NOT NULL,
  grade VARCHAR(2),
  PRIMARY KEY (id, class_id),
  FOREIGN KEY (id) REFERENCES students (id),
  FOREIGN KEY (class_id) REFERENCES classes (class_id)
);

CREATE TABLE teaches (
  id INT NOT NULL,
  class_id INT NOT NULL,
  PRIMARY KEY (id, class_id),
  FOREIGN KEY (id) REFERENCES teachers (id),
  FOREIGN KEY (class_id) REFERENCES classes (class_id)
);

/*AUXILARY TABLES*/
CREATE TABLE female_names (name VARCHAR(100));

CREATE TABLE male_names (name VARCHAR(100));

CREATE TABLE last_names (name VARCHAR(100));

CREATE TABLE addresses (
  addr VARCHAR(50),
  city VARCHAR(30),
  state VARCHAR(3),
  zip INT
);
