import pickle
import time

import mysql.connector
import psycopg2
import redis
from elasticsearch import Elasticsearch

from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from pymongo import MongoClient

es = Elasticsearch(
	'https://localhost:9200',
	basic_auth=('elastic', 'elastic'),
	verify_certs=False
)

numbers_processed_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Numbers-Processed',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: pickle.loads(x)
)

try:
    numbers_processed_partition = TopicPartition('Numbers-Processed', 0)
    numbers_processed_consumer.assign([numbers_processed_partition])
    numbers_processed_consumer.position(numbers_processed_partition)
except Exception:
    pass

print('Waiting for messages via Numbers-Processed...')

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="Numeralia",
    connection_timeout=5
)

mysql_db_cursor = mysql_db.cursor()

for TopicPartition, ConsumerRecord in (
        numbers_processed_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        print('Inserting into MySQL DB...')

        mysql_db_cursor.execute(
            'INSERT INTO Records (Number, Spelling) VALUES (%s, %s)',
            (
                message.value[0], message.value[1]
            )
        )

        mysql_db.commit()

        es.index(
            index='numbers',
            document={
                'Number': message.value[0],
                'When': time.time(),
                'What': 'archived',
            },
        )

mysql_db.close()
numbers_processed_consumer.close()

dots_processed_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Dots-Processed',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: pickle.loads(x)
)

try:
    dots_processed_partition = TopicPartition('Dots-Processed', 0)
    dots_processed_consumer.assign([dots_processed_partition])
    dots_processed_consumer.position(dots_processed_partition)
except Exception:
    pass

print('Waiting for messages via Dots-Processed...')

postgres_db = psycopg2.connect(
    host="localhost",
    database="Numeralia",
    user="postgres",
    connect_timeout=5
)

postgres_db_cursor = postgres_db.cursor()

for TopicPartition, ConsumerRecord in (
        dots_processed_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        print('Inserting into Postgres DB...')

        postgres_db_cursor.execute(
            'INSERT INTO Records (Number, Sequence) VALUES (%s, %s)',
            (
                message.value[0], message.value[1]
            )
        )

        postgres_db.commit()

        es.index(
            index='dots',
            document={
                'Number': message.value[0],
                'When': time.time(),
                'What': 'archived',
            },
        )

postgres_db.close()
dots_processed_consumer.close()

increasing_processed_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Increasing-Processed',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: pickle.loads(x)
)

try:
    increasing_processed_partition = TopicPartition('Increasing-Processed', 0)
    increasing_processed_consumer.assign([increasing_processed_partition])
    increasing_processed_consumer.position(increasing_processed_partition)
except Exception:
    pass

print('Waiting for messages via Increasing-Processed...')

r = redis.Redis()

for TopicPartition, ConsumerRecord in (
        increasing_processed_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        print('Inserting into Redis DB...')

        r.set(message.value[0], str(message.value[1]))

        es.index(
            index='increasing',
            document={
                'Number': message.value[0],
                'When': time.time(),
                'What': 'archived',
            },
        )

r.close()
increasing_processed_consumer.close()

binary_processed_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Binary-Processed',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: pickle.loads(x)
)

try:
    binary_processed_partition = TopicPartition('Binary-Processed', 0)
    binary_processed_consumer.assign([binary_processed_partition])
    binary_processed_consumer.position(binary_processed_partition)
except Exception:
    pass

print('Waiting for messages via Binary-Processed...')

client = MongoClient(username='admin', password='admin')

db = client['Numeralia']
collection = db['Records']

for TopicPartition, ConsumerRecord in (
        binary_processed_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        print('Inserting into MongoDB...')

        collection.insert_one({
            'Number': message.value[0],
            'Binary': message.value[1]
        })

        es.index(
            index='binary',
            document={
                'Number': message.value[0],
                'When': time.time(),
                'What': 'archived',
            },
        )

client.close()
binary_processed_consumer.close()
es.close()
