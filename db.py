'''PURPOSE: CREATE A DATABASE  
    DATE: 5/8/2021
    AUTOR: Martin Benko
'''
import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='mbenko', password='mbenko', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''CREATE database frinxPy''';

#Creating a database
cursor.execute(sql)
print("Database created successfully........")

#Closing the connection
conn.close()


