"""Consumer class definition."""

from typing import Callable, Literal

from retrying import retry

import kafka


class Consumer(kafka.KafkaConsumer):
	"""Consumer class.

	This class inherits from KafkaConsumer and customizes its functionality.

	In particular, it allows for the consumption of messages from Kafka topics.
	It handles those incoming messages and returns the relevant parts.

	Instances are initialized in the same way as KafkaConsumer.

	"""
	# The retry decorator is helpful for dealing with possible intermittent
	# connection issues. It prevents the container from crashing entirely and
	# thus makes the application more fault-tolerant.
	@retry(wait_fixed=5000, stop_max_attempt_number=12)
	def __init__(
			self,
			topic: Literal[
				'Numbers', 'Numbers-Processed'
			],
			group_id: Literal[
				'processors', 'archiver'
			],
			value_deserializer: Callable[
				[bytes], int
			]
	) -> None:
		"""Initialize the KafkaConsumer instance with the given values.

		Consumers will poll a maximum of 1 (one) record in this application.

		"""
		super().__init__(
			topic,
			bootstrap_servers='localhost:9092',
			group_id=group_id,
			max_poll_records=1,
			value_deserializer=value_deserializer
		)

	def consume(self) -> kafka.consumer.fetcher.ConsumerRecord:
		"""Consume messages from this client's Kafka topic.

		This method will poll the Kafka topic (through the Kafka Broker) to
		fetch one (1) message from it. KafkaConsumer.poll() is a blocking call
		with a timeout of 45 seconds.

		:return: Consumed message in the form of a ConsumerRecord object.
		"""
		print('Waiting for a message...')

		# Poll the topic to fetch 1 record.
		_, ConsumerRecord = [
			poll for poll in super().poll(timeout_ms=45000).items()
		][0]

		# The discarded parts are metadata not used by this application.
		ConsumerRecord = ConsumerRecord[0]

		print(f'Received {ConsumerRecord.value} via {ConsumerRecord.topic}')

		return ConsumerRecord
