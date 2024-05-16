from random import randrange

from kafka import KafkaProducer

producer = KafkaProducer(
	bootstrap_servers='localhost:9092',
	value_serializer=lambda x: x.to_bytes((x.bit_length() + 7) // 8, 'big')
)

number_numbers = randrange(5000)

print(f'Sending {number_numbers} to Numbers...')

producer.send(
	topic='Numbers',
	value=number_numbers
)

number_dots = randrange(80)

print(f'Sending {number_dots} to Dots...')

producer.send(
	topic='Dots',
	value=number_dots
)

number_increasing = randrange(10)

print(f'Sending {number_increasing} to Increasing...')

producer.send(
	topic='Increasing',
	value=number_increasing
)

number_binary = randrange(65000)

print(f'Sending {number_binary} to Binary...')

producer.send(
	topic='Binary',
	value=number_binary
)

producer.close()
