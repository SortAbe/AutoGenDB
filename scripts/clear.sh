#!/usr/bin/env bash

cat << EOF | mysql
USE University;
TRUNCATE TABLE teaches;
TRUNCATE TABLE takes;
TRUNCATE TABLE teachers_address;
TRUNCATE TABLE teachers_contact;
TRUNCATE TABLE students_contact;
TRUNCATE TABLE students_address;
DELETE FROM students WHERE TRUE;
DELETE FROM classes WHERE TRUE;
DELETE FROM teachers WHERE TRUE;
PURGE BINARY LOGS BEFORE NOW();
COMMIT;
EOF
