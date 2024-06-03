"""Indexer class definition."""

import time

from elasticsearch import Elasticsearch

from retrying import retry


class Indexer(Elasticsearch):
	"""Indexer class.

	This class inherits from Elasticsearch and customizes its functionality.

	In particular, it allows for the indexing of documents into Elasticsearch
	with the specific structure that this application expects.

	Instances are initialized in the same way as Elasticsearch. Instantiation
	takes no arguments since these are preset in the init.

	"""
	# The retry decorator is helpful for dealing with possible intermittent
	# connection issues. It prevents the container from crashing entirely and
	# thus makes the application more fault-tolerant.
	@retry(wait_fixed=5000, stop_max_attempt_number=12)
	def __init__(self):
		"""Initialize the Elasticsearch client."""
		super().__init__(
			'https://localhost:9200',
			basic_auth=('elastic', 'elastic'),
			verify_certs=False  # for simplicity
		)

	def index_record(
			self, number: int, what: str, index: str
	) -> None:
		"""Index a record.

		This method indexes a custom document into the Elasticsearch using the
		Elasticsearch.index() method.

		"""
		print(f'Indexing {number} to {index}...')

		super().index(
			index=index,
			document={
				'Number': number,
				'When': time.time(),
				'What': what,
			}
		)
