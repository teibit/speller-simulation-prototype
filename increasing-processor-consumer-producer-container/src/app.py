import pickle
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer, KafkaProducer, TopicPartition

increasing_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Increasing',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: int.from_bytes(x, 'big')
)

es = Elasticsearch(
	'https://localhost:9200',
	basic_auth=('elastic', 'elastic'),
	verify_certs=False
)

increasing_consumer.assign([TopicPartition('Increasing', 0)])
increasing_consumer.position(TopicPartition('Increasing', 0))

print('Waiting for messages...')

for TopicPartition, ConsumerRecord in (
        increasing_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        increasing_processed_producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: pickle.dumps(x)
        )

        print('Processing and producing to broker via Increasing-Processed...')

        increasing_processed_producer.send(
            topic='Increasing-Processed',
            value=(
                message.value,
                [x for x in range(message.value)]
            )
        )

        es.index(
            index='increasing',
            document={
                'Number': message.value,
                'When': time.time(),
                'What': 'processed',
            },
        )

        increasing_processed_producer.close()

increasing_consumer.close()
es.close()
