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

select * from student 
join takes on student.ID = takes.ID
where student.ID = 400;

select * from student
join sAddress on sAddress.ID = student.ID
join sContact on sContact.ID = student.ID
where dept_name rlike 'Department of (History|Physics)'
and firstName like 'Abraham'
and state in ('CA', 'TN');

update student set firstName = 'Abraham' where firstName like 'Abrahan';
