import pickle
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer, KafkaProducer, TopicPartition

dots_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Dots',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: int.from_bytes(x, 'big')
)

es = Elasticsearch(
	'https://localhost:9200',
	basic_auth=('elastic', 'elastic'),
	verify_certs=False
)

dots_consumer.assign([TopicPartition('Dots', 0)])
dots_consumer.position(TopicPartition('Dots', 0))

print('Waiting for messages...')

for TopicPartition, ConsumerRecord in (
        dots_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        dots_processed_producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: pickle.dumps(x)
        )

        print('Processing and producing to broker via Dots-Processed...')

        dots_processed_producer.send(
            topic='Dots-Processed',
            value=(
                message.value,
                '.' * message.value
            )
        )

        es.index(
            index='dots',
            document={
                'Number': message.value,
                'When': time.time(),
                'What': 'processed',
            },
        )

        dots_processed_producer.close()

dots_consumer.close()
es.close()
