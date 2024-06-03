"""Inputter module.

This script simulates messages coming into the app over time. Those messages
are ints sent to a specific Kafka topic, to be later picked up by the Speller.
This abstracts away the generation of messages into the app's pipelines.

"""
from random import randrange
from time import sleep

from src.common.producer import Producer


def input() -> None:
	"""Input data into the app's pipelines.

	This method generates random ints to be sent to the appropriate Kafka
	topic. The actual publishing into the broker is done by the Producer.
	It also indexes this 'produced' event in ElasticSearch.

	"""
	# Get a Producer object that communicates with localhost:9092.
	producer = Producer(
		# Serialize an int into a byte. This producer will produce ints,
		# but those will be represented internally as bytes during
		# communication with the broker.
		value_serializer=(
			lambda x: x.to_bytes((x.bit_length() + 7) // 8, 'big')
		)
	)

	# Produce to the Kafka topic (and its respective ES index).
	# Note that the Kafka topic starts with capital, which aris unsupported in
	# ES indexes. Hence the two versions and the use of str.lower().
	data = randrange(1000000)
	topic: str = 'Numbers'

	producer.produce(
		data=data, topic=topic, index=topic.lower()
	)

	print()

	# Close Kafka producer (and related Elasticsearch client).
	producer.terminate()

	# Take a break before inputting all over again.
	sleep(30)


def main() -> None:
	"""Main function.

	This script will insert input into the app's pipelines continuously.

	More specifically, it will generate data to the 4 main topics using a
	Producer object and then take a break.

	The Producer object is created and destroyed on each iteration,
	simulating different producers connecting to the Kafka broker and
	generating their due data.

	"""
	print('Beginning inputting...\n')

	# Minimum wait for ElasticSearch to begin accepting connections.
	# The container will crash if this wait is not respected.
	sleep(30)

	# Input indefinitely.
	while True:
		input()


if __name__ == '__main__':
	main()
