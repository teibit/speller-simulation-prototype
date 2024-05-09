from random import randrange

from kafka import KafkaProducer

producer = KafkaProducer(
	bootstrap_servers='localhost:9092',
	value_serializer=lambda x: x.to_bytes((x.bit_length() + 7) // 8, 'big')
)

number = randrange(5000)

print(f'Sending {number} to Numbers...')

producer.send(
	topic='Numbers',
	value=number
)

number = randrange(80)

print(f'Sending {number} to Dots...')

producer.send(
	topic='Dots',
	value=number
)

producer.close()
