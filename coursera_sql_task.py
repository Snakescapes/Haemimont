# import pyodbc
import csv, sqlite3
from datetime import datetime

student_pins_to_check = input("Which students would you like to check? Please list PINs (comma separated): ").split(', ')
minimum_credit = int(input('Enter required minimum credit: '))
start_date = datetime.strptime(input('Please enter start date (format Year-Month-Day e.g. 18-12-31): '), '%y%m%d').date()
end_date = datetime.strptime(input('Please enter end date (format Year-Month-Day e.g. 18-12-31): '), '%y%m%d').date()
output_format = input('Please choose output format (html/csv). If none chosen, both will be generated.')
directory_path = input('Please select output directory path: ')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-SS7I0B0\SQLEXPRESS;'
                      'Database=coursera;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('''
SQL query blueprint:

DECLARE @Pin VARCHAR(10)
SET @Pin = {0}
DECLARE @StartDate date
SET @StartDate = CONVERT(datetime, CONVERT(VARCHAR(8), {1}))
DECLARE @EndDate date
SET @EndDate = CONVERT(datetime, CONVERT(VARCHAR(8), {2}))

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
'''.format(student_pins_to_check, start_date, end_date))


if output_format == "csv" or '':
    with open('student_report.csv', mode='w') as report:
        report_writer = csv.writer(report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)