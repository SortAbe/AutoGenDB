select count(*) from department;
select count(*) from femaleNames;
select count(*) from maleNames;
select count(*) from instructor;
select count(*) from student;
select count(*) from sAddress;
select count(*) from sContact;
select count(*) from tAddress;
select count(*) from tContact;
select count(*) from takes;
select count(*) from teaches;

select * from student where firstName like 'Abrahan';

select * from student where ID = 777777;
select * from student where ID like 777777;

select max(ID) from student;

select student.firstName, student.lastName,
student.dept_name, course.title, class.semester, class.year
from student
join takes on student.ID = takes.ID
join class on class.class_id = takes.class_id
join course on class.course_id = course.course_id
where student.ID = 400;

select * from student
join sAddress on sAddress.ID = student.ID
join sContact on sContact.ID = student.ID
where dept_name rlike 'Department of (History|Physics)'
and firstName like 'Abraham'
and state in ('CA', 'TN');

update student set firstName = 'Abraham' where firstName like 'Abrahan';

select * from teachers where salary = (select max(salary) from teachers);
select * from teachers where salary = (select round(avg(salary)) from teachers);

select * from students where credits = (select max(credits) from students) limit 40;
select * from students where credits = (select round(avg(credits)) from students) limit 40;

select MAX(salary) from teachers;
