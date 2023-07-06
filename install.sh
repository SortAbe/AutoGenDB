#!/bin/bash

echo "Some details are needed!"
echo "What is your database address/domain?"
read db_host
echo "What is your database port?"
read db_port
echo "What is your database user?"
read db_user
echo "what is your database password?"
read db_password

host=$db_host
user=$db_user
port=$db_port
password=$db_password

export host
export user
export port
export password

sudo apt update
sudo apt install python3-pip
pip3 install random-address
pip3 install mysql-connector-python

cat ./sqlfiles/schema.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/department.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/course.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/female.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/male.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/last.sql >> ./sqlfiles/complete.sql

mysql -u $db_user -h $db_host -P $db_port -p < ./sqlfiles/complete.sql
rm -f ./sqlfiles/complete.sql
