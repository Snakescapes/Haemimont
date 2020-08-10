import pyodbc
from datetime import datetime

student_pins_to_check = input("Which students would you like to check? Please list PINs (comma separated): ").split(', ')
minimum_credit = int(input('Enter required minimum credit: '))
start_date = datetime.strptime(input('Please enter start date (format Year-Month-Day e.g. 18-12-31): '), '%y%m%d').date()
end_date = datetime.strptime(input('Please enter end date (format Year-Month-Day e.g. 18-12-31): '), '%y%m%d').date()
output_format = input('Please choose output format (html/csv). If none chosen, both will be generated.')
directory_path = input('Please select output directory path: ')

'''
SQL query blueprint:

DECLARE @Pin VARCHAR(10)
SET @Pin = student_pins_to_check
DECLARE @StartDate date
SET @StartDate = CONVERT(datetime, CONVERT(VARCHAR(8), start_date))
DECLARE @EndDate date
SET @EndDate = CONVERT(datetime, CONVERT(VARCHAR(8), end_date))

SELECT s.first_name + ' ' + s.last_name as 'Student',
 c.[name] as 'Course Name', c.total_time as 'Total  time', c.credit as 'Credit',
 i.first_name + ' ' + i.last_name as 'Instructor', sum(c.credit) as 'Total Credits'
INTO Result_Table
FROM students as s
JOIN students_courses_xref as sc
ON s.pin = sc.student_pin
JOIN courses as c
ON  sc.course_id = c.id
JOIN instructors as i
ON c.instructor_id = i.id
WHERE student_pin = @Pin AND sc.completion_date >= @StartDate AND sc.completion_date <= @EndDate
GROUP BY s.first_name, s.last_name, c.[name], c.total_time, c.credit, i.first_name, i.last_name
'''
