import sqlite3

## Connectt to SQlite
connection=sqlite3.connect("student.db")

## Create a cursor object to insert record,create table

cursor=connection.cursor()

## create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)

## Inserting sample Records into Table

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','B',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','A',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data Science','B',75)''')
cursor.execute('''Insert Into STUDENT values('Vikas','DEVOPS','D',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','C',39)''')

cursor.execute('''Insert Into STUDENT values('Amruta','Maths','A',90)''')
cursor.execute('''Insert Into STUDENT values('Aarushi','Social science','B',77)''')
cursor.execute('''Insert Into STUDENT values('Neha','English','A',99)''')
cursor.execute('''Insert Into STUDENT values('Sunil','Maths','C',35)''')

## Displaying All the records

print("The isnerted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit in the databse
connection.commit()
connection.close()