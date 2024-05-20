import time
from random import randrange

from elasticsearch import Elasticsearch
from kafka import KafkaProducer

producer = KafkaProducer(
	bootstrap_servers='localhost:9092',
	value_serializer=lambda x: x.to_bytes((x.bit_length() + 7) // 8, 'big')
)

es = Elasticsearch(
	'https://localhost:9200',
	basic_auth=('elastic', 'elastic'),
	verify_certs=False
)

number_numbers = randrange(5000)

print(f'Sending {number_numbers} to Numbers...')

producer.send(
	topic='Numbers',
	value=number_numbers
)

es.index(
	index='numbers',
	document={
		'Number': number_numbers,
		'When': time.time(),
		'What': 'produce',
	},
)

number_dots = randrange(80)

print(f'Sending {number_dots} to Dots...')

producer.send(
	topic='Dots',
	value=number_dots
)

es.index(
	index='dots',
	document={
		'Number': number_dots,
		'When': time.time(),
		'What': 'produce',
	},
)

number_increasing = randrange(10)

print(f'Sending {number_increasing} to Increasing...')

producer.send(
	topic='Increasing',
	value=number_increasing
)

es.index(
	index='increasing',
	document={
		'Number': number_increasing,
		'When': time.time(),
		'What': 'produce',
	},
)

number_binary = randrange(65000)

print(f'Sending {number_binary} to Binary...')

producer.send(
	topic='Binary',
	value=number_binary
)

es.index(
	index='binary',
	document={
		'Number': number_binary,
		'When': time.time(),
		'What': 'produce',
	},
)

producer.close()
es.close()
