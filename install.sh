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
export db_host

pip3 install random-address

export db_port
export db_user
export db_password

cat ./sqlfiles/schema.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/department.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/course.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/females.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/males.sql >> ./sqlfiles/complete.sql
cat ./sqlfiles/last.sql >> ./sqlfiles/complete.sql

mysql -u $db_user -h $db_host -P $db_port -p < ./sqlfiles/complete.sql
rm -f ./sqlfiles/complete.sql

