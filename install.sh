#!/bin/bash

#python3 -m pip install mysql-connector-python

{
cat ./sqlfiles/schema.sql
cat ./sqlfiles/department.sql
cat ./sqlfiles/course.sql
cat ./sqlfiles/addr.sql
cat ./sqlfiles/female.sql
cat ./sqlfiles/male.sql
cat ./sqlfiles/last.sql
echo 'COMMIT'
} >> ./sqlfiles/complete.sql

mysql -u py -h localhost -pxKHOxyThyC7u8f < ./sqlfiles/complete.sql
rm -f ./sqlfiles/complete.sql
