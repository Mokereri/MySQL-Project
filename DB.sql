-- Create a database named edu_institute.

CREATE DATABASE edu_institute


#--Within edu_institute, create a table named students

USE edu_institute;
CREATE TABLE students(
student_id INT PRIMARY KEY,
name VARCHAR(50),
age INT,
gender CHAR(1),
enrollment_date DATE,
program VARCHAR(50)
);


#--Insert at least 5 records into the students table, with diverse names, ages, genders, enrolment dates, and programs. Ensure at least one student is enrolled in "Data Science".

INSERT INTO students (student_id, name, age, gender, enrollment_date, program)
VALUES 
	(1, 'Skido Matiko', 25, 'M', '2024/01/01', 'Computer science'),
	(2, 'Marvin Mboya', 27, 'M', '2024/01/02', 'Data science'),
	(3, 'Brenda Aida', 23, 'F', '2024/01/02', 'Data Analytics'),
	(4, 'Mokereri Kelvin', 25, 'M', '2024/01/01', 'Data science'),
	(5, 'Rediet Hadera', 22, 'F', '2024/01/01', 'Computer science'),
	(6, 'Ayra starr', 21, 'F', '2024/01/03', 'Data Analytics'),
	(7, 'Edmund Opiyo', 26, 'M', '2024/01/01', 'Software Engineering'),
	(8, 'Sharlene Anyango', 22, 'F', '2024/01/02', 'Data science'),
	(9, 'Faith Robi', 21, 'F', '2024/01/01', 'Software Engineering'),
	(10, 'Ken Mwijaku', 20, 'M', '2024/01/02', 'Cyber security')

#--Write a query to select all columns for all students in the "Data Science" program.

SELECT * 
FROM students
WHERE program = 'Data science';


#--Write a query to find the total number of students and display it as Total Students.

SELECT COUNT(name) AS 'Total students'
FROM students


#--Use an appropriate function to display the current date in a column named Today's Date

SELECT CURRENT_DATE() AS "Today's Date";


#-Write a query to select the student names and their enrolment dates, but display the name column in uppercase.

SELECT UPPER(name) AS Student_name, enrollment_date
FROM students;


#--Write a query to count the number of students in each program and display the results in descending order 

SELECT COUNT(name) AS 'Number of students', program
FROM students
GROUP BY program
ORDER BY COUNT(name) DESC


#--Write a query to find the youngest student's name and age.
SELECT name, age
FROM students 
ORDER BY age ASC
LIMIT 1;
