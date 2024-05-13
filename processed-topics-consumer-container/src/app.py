import pickle

import mysql.connector
import psycopg2

from kafka import KafkaConsumer, TopicPartition

numbers_processed_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Numbers-Processed',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: pickle.loads(x)
)

numbers_processed_partition = TopicPartition('Numbers-Processed', 0)
numbers_processed_consumer.assign([numbers_processed_partition])
numbers_processed_consumer.position(numbers_processed_partition)

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

mysql_db.close()
numbers_processed_consumer.close()

dots_processed_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Dots-Processed',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: pickle.loads(x)
)

dots_processed_partition = TopicPartition('Dots-Processed', 0)
dots_processed_consumer.assign([dots_processed_partition])
dots_processed_consumer.position(dots_processed_partition)

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

postgres_db.close()
dots_processed_consumer.close()
