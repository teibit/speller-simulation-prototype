from random import randrange

from kafka import KafkaProducer

producer = KafkaProducer(
	bootstrap_servers='localhost:9092',
	value_serializer=lambda x: x.to_bytes((x.bit_length() + 7) // 8, 'big')
)

message = randrange(100)

print(f'Sending {message} to Numbers...')

producer.send(
	topic='Numbers',
	value=message
)

producer.close()
