from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='Numbers',
    max_poll_records=1,
    request_timeout_ms=11000,
    value_deserializer=lambda x: int.from_bytes(x, 'big')
)

consumer.assign([TopicPartition('Numbers', 0)])
consumer.position(TopicPartition('Numbers', 0))

print('Waiting for messages...')

for TopicPartition, ConsumerRecord in (
        consumer.poll(timeout_ms=5000).items()
):
    for message in ConsumerRecord:
        print(f'Received {message.value} via {message.topic}')

consumer.close()
