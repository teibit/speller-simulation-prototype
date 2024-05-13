import pickle

import inflect

from kafka import KafkaConsumer, KafkaProducer, TopicPartition

numbers_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Numbers',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: int.from_bytes(x, 'big')
)

numbers_consumer.assign([TopicPartition('Numbers', 0)])
numbers_consumer.position(TopicPartition('Numbers', 0))

print('Waiting for messages...')

for TopicPartition, ConsumerRecord in (
        numbers_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        numbers_processed_producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: pickle.dumps(x)
        )

        print('Processing and producing to broker via Numbers-Processed...')

        numbers_processed_producer.send(
            topic='Numbers-Processed',
            value=(
                message.value,
                inflect.engine().number_to_words(message.value)
            )
        )

        numbers_processed_producer.close()

numbers_consumer.close()
