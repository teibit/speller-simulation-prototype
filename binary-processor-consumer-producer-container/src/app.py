import pickle

from kafka import KafkaConsumer, KafkaProducer, TopicPartition

binary_consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Binary',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: int.from_bytes(x, 'big')
)

binary_consumer.assign([TopicPartition('Binary', 0)])
binary_consumer.position(TopicPartition('Binary', 0))

print('Waiting for messages...')

for TopicPartition, ConsumerRecord in (
        binary_consumer.poll(timeout_ms=5000).items()
):

    for message in ConsumerRecord:

        print(f'Received {message.value} via {message.topic}')

        binary_processed_producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: pickle.dumps(x)
        )

        print('Processing and producing to broker via Binary-Processed...')

        binary_processed_producer.send(
            topic='Binary-Processed',
            value=(
                message.value,
                bin(message.value)
            )
        )

        binary_processed_producer.close()

binary_consumer.close()
