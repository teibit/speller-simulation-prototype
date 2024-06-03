"""Producer class definition."""

from typing import Callable, Tuple, Union

from kafka import KafkaProducer

from retrying import retry

from src.common.indexer import Indexer


class Producer(KafkaProducer):
	"""Producer class.

	This class inherits from KafkaProducer and customizes its functionality.

	In particular, it allows for the production of messages into Kafka topics.

	It also handles the logging of these production events in ElasticSearch.

	Instances are initialized in the same way as KafkaProducer.

	"""
	es: Indexer = None

	# The retry decorator is helpful for dealing with possible intermittent
	# connection issues. It prevents the container from crashing entirely and
	# thus makes the application more fault-tolerant.
	@retry(wait_fixed=5000, stop_max_attempt_number=12)
	def __init__(
			self, value_serializer: Callable[[int], bytes]
	) -> None:
		"""Initialize the KafkaProducer object and the Elasticsearch client."""
		super().__init__(
			bootstrap_servers='localhost:9092',
			value_serializer=value_serializer,
			connection_timeout_ms=120000
		)

		# Indexer instance to index production events in ElasticSearch.
		self.es = Indexer()

	def produce(
			self, data: Union[int, Tuple[int, str]],
			topic: str, index: str,
			what: str = 'produced'
	) -> None:
		"""Produce data to the Kafka Broker.

		This method will send the provided data, which could be presented in the
		form of an integer or a tuple of an integer and a string, to the
		specified topic.

		It will also index this producing event in ElasticSearch using the
		Indexer object. Notice that this action happens automatically as a side
		effect in a way that is completely transparent to the caller.

		"""
		print(f'Producing {data} to {topic}...')

		super().send(topic, data)

		# Only numbers (app's input) are indexed, so data is processed
		# accordingly: if it's already a number, index it directly; if it's a
		# tuple, use its first member and discard the rest.
		self.es.index_record(
			data if isinstance(data, int) else data[0], what, index
		)

	def terminate(self) -> None:
		"""Close the Kafka producer and the Elasticsearch client."""
		super().close()
		self.es.close()
