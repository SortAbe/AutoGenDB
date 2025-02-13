#!/bin/bash

echo "Some details are needed!"
echo "What is your database address/domain?"
read dbhost
echo "What is your database user?"
read dbuser
echo "What is your database port?"
read dbport
echo "what is your database password?"
read dbpassword

echo -e "export db_host=$dbhost" >> ~/.bashrc
echo -e "export db_user=$dbuser" >> ~/.bashrc
echo -e "export db_port=$dbport" >> ~/.bashrc
echo -e "export db_password=$dbpassword" >> ~/.bashrc
source ~/.bashrc

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
