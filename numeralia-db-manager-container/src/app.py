import mysql.connector
import psycopg2

mysql_db = mysql.connector.connect(
  host='localhost',
  user='root'
)

mysql_db_cursor = mysql_db.cursor()

mysql_db_cursor.execute('CREATE DATABASE IF NOT EXISTS Numeralia;')

mysql_db_cursor.execute('USE Numeralia;')

mysql_db_cursor.execute(
  'CREATE TABLE IF NOT EXISTS Numeralia.Records('
    'Number INTEGER,'
    'Spelling VARCHAR(255)'
  ');'
)

mysql_db_cursor.execute('DESCRIBE Numeralia.Records;')

print('MySQL')

mysql_db_cursor.execute('SELECT * FROM Numeralia.Records;')

for row in mysql_db_cursor.fetchall():
  print(row)

postgres_db = psycopg2.connect(
  host="localhost",
  user="postgres",
  database="Numeralia"
)

postgres_db_cursor = postgres_db.cursor()

print('\nPostgres')

postgres_db_cursor.execute('SELECT * FROM Records;')

for row in postgres_db_cursor.fetchall():
  print(row)
