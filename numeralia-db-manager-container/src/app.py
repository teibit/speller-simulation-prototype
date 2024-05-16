import mysql.connector
import psycopg2
import redis
from pymongo import MongoClient

mysql_db = mysql.connector.connect(
  host='localhost',
  user='root'
)

mysql_db_cursor = mysql_db.cursor(buffered=True)

mysql_db_cursor.execute('CREATE DATABASE IF NOT EXISTS Numeralia;')

mysql_db_cursor.execute('USE Numeralia;')

mysql_db_cursor.execute(
  'CREATE TABLE IF NOT EXISTS Numeralia.Records('
    'Number INTEGER,'
    'Spelling VARCHAR(255)'
  ');'
)

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

r = redis.Redis()

keys = r.keys()

print('\nRedis')

# Get all values associated with the keys
for key in keys:
  print(f'({key}, {r.get(key)})')

r.close()

client = MongoClient(username='admin', password='admin')

db = client['Numeralia']
collection = db['Records']

print('\nMongoDB')
for record in collection.find():
  print(record)
