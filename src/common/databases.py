"""Databases common module.

This module provides common functionality for all databases used by this
application.

It defines a hierarchy of classes lingering on the SQL vs NoSQL database
classification.

The MySQL & Postgres database classes inherit from the SQL class. The Redis &
Mongo database classes, as well as the parent SQL class, inherit from the
general base Database class. So, the relations are:

Database <- SQL <- MySQL
Database <- SQL <- Postgres
Database <- Redis
Database <- Mongo

These classes are helpful in customizing the core functionality of the main
db classes they're based on. In particular, they allow for the integration with
Indexer objects for ElasticSearch logging.

"""
from abc import ABC, abstractmethod
from typing import Union

# Core database modules of this application.
import mysql.connector
import psycopg2  # Postgres
import redis
from pymongo import MongoClient

from src.common.indexer import Indexer


class Database(ABC):
	"""Base Database class.

	This is an abstract base class that establishes a common interface for all
	database classes to follow.

	In particular, each database object should provide a way to store data,
	observe the current state of the database, and terminate it.

	"""
	# A Database-derived object must have a MySQL, Postgres, Redis or Mongo
	# client.
	client: Union[
		mysql.connector.connection_cext.CMySQLConnection,
		psycopg2.extensions.connection,
		redis.Redis,
		MongoClient
	] = None

	es: Indexer = None

	host: str = 'localhost'
	connection_timeout: int = 30  # seconds

	@abstractmethod
	def store(
			self,
			number: int,
			processed: str,
			index: str
	) -> None:
		pass

	@abstractmethod
	def observe(self) -> None:
		pass

	def terminate(self) -> None:
		"""Close the DB and Elasticsearch clients."""
		self.client.close()
		self.es.close()


class Redis(Database):
	"""Redis database class.

	This class provides a familiar interface for communicating with Redis
	within this application.

	It provides a specific implementation for storing data in a Redis database,
	as well as observing the current state of the database, using the
	redis.Redis module.

	It also handles ES indexing of the production events.

	"""
	def __init__(self):
		"""Initialize the Redis database (and associated Indexer)."""
		self.client = redis.Redis()
		self.es = Indexer()

	def store(
			self,
			number: int,
			processed: str,
			index: str
	) -> None:
		"""Store data in the Redis database.

		This method will store (number, processed) in the Redis database by
		using the redis.Redis.set() method.

		It will also index this 'archived-Redis' event in ES.

		:param number: Input from Inputter.
		:param processed: Output from Speller.
		:param index: ES index for this 'archived-Redis' event.

		"""
		self.client.set(str(number), processed)

		self.es.index_record(
			number=number, what='archived-Redis', index=index
		)

	def observe(self) -> list:
		"""Observe the current state of the database.

		This method will return a snapshot showing the current state of the
		database.

		:return: A list of all the (number, processed) tuples in the database.

		"""
		return [
			(key, self.client.get(key))
			for key in self.client.keys()
		]


class Mongo(Database):
	"""Mongo database class.

	This class provides a familiar interface for communicating with Mongo
	within this application.

	It provides a specific implementation for storing data in a Mongo database,
	as well as observing the current state of the database, using the
	MongoClient package.

	It also handles ES indexing of the production events.

	"""
	def __init__(self):
		"""Initialize the Mongo client (and associated Indexer)."""
		self.client = MongoClient(
			username='admin', password='admin'
		)
		self.es = Indexer()

	def store(
			self,
			number: int,
			processed: str,
			index: str
	) -> None:
		"""Store data in the Mongo database.

		This method will store (number, processed) in the Mongo database by
		using the MongoClient.insert_one() method. It will define the database
		as Numeralia and the table as Records.

		It will also index this 'archived-Mongo' event in ES.

		:param number: Input from Inputter.
		:param processed: Output from Speller.
		:param index: ES index for this 'archived-Mongo' event.

		"""
		self.client['Numeralia']['Records'].insert_one({
			'Number': number,
			'Spelling': processed
		})

		self.es.index_record(
			number=number, what='archived-Mongo', index=index
		)

	def observe(self) -> list:
		"""Observe the current state of the database.

		This method will return a snapshot showing the current state of the
		database.

		:return: A list of all the (number, processed) tuples in the database.

		"""
		return [
			(record['Number'], record['Spelling'])
			for record in self.client['Numeralia']['Records'].find()
		]


class SQL(Database):
	"""SQL base class."""
	# SQL query for storing.
	sql: str = None

	# Notice that only SQL DBs have cursors.
	cursor: Union[
		mysql.connector.cursor_cext.CMySQLCursor,
		psycopg2.extensions.cursor
	] = None

	def observe(self) -> list:
		"""Observe the current state of the database.

		This method will return a snapshot showing the current state of the
		database.

		:return: A list of all the (number, processed) tuples in the database.

		"""
		self.cursor.execute(
			open('sql/select-all.sql').read()
		)

		return self.cursor.fetchall()


class MySQL(SQL):
	"""MySQL database class.

	This class provides a familiar interface for communicating with MySQL
	within this application.

	It provides a specific implementation for storing data in a MySQL database,
	as well as observing the current state of the database, using the
	mysql.connector module.

	It also handles ES indexing of the production events.

	"""
	def __init__(self):
		"""Initialize the MySQL client (and associated Indexer).

		This method initializes the MySQL client and related objects. It also
		actually initializes the database by executing some initialization SQL
		scripts.

		"""
		self.client = mysql.connector.connect(
			host=self.host,
			user='root',
			connection_timeout=self.connection_timeout
		)
		self.cursor = self.client.cursor()

		# Execute initialization scripts to set up the DB & table.
		self.cursor.execute(
			open('sql/create-db-mysql.sql').read()
		)
		self.cursor.execute(
			open('sql/use-db.sql').read()
		)
		self.cursor.execute(
			open('sql/create-table.sql').read()
		)

		self.sql = open('sql/insert.sql').read()

		self.es = Indexer()

	def store(
			self,
			number: int,
			processed: str,
			index: str
	) -> None:
		"""Store data in the MySQL database.

		This method will store (number, processed) in the MySQL database by
		executing the insert SQL script in the client's cursor and committing
		the changes to the database.

		It will also index this 'archived-MySQL' event in ES.

		:param number: Input from Inputter.
		:param processed: Output from Speller.
		:param index: ES index for this 'archived-Mongo' event.

		"""
		self.cursor.execute(
			self.sql, (number, processed)
		)

		self.client.commit()

		self.es.index_record(
			number=number, what='archived-MySQL', index=index
		)


class Postgres(SQL):
	"""Postgres database class.

	This class provides a familiar interface for communicating with Postgres
	within this application.

	It provides a specific implementation for storing data in a Postgres
	database, as well as observing the current state of the database, using the
	psycopg2 module.

	It also handles ES indexing of the production events.

	"""
	def __init__(self):
		"""Initialize the Postgres client (and associated Indexer).

		This method initializes the Postgres client and related objects. It also
		actually initializes the database by executing some initialization SQL
		scripts.

		"""
		self.client = psycopg2.connect(
			host=self.host,
			user='postgres',
			connect_timeout=self.connection_timeout
		)
		self.cursor = self.client.cursor()

		# Unfortunately psycopg2's SQL does NOT support "IF NOT EXISTS" on
		# "CREATE DATABASE" statements, so we must work around this by manually
		# checking if it exists first.
		self.cursor.execute(
			open('sql/check-db-exists.sql').read()
		)

		# Create the database anew only if it doesn't exist.
		if not self.cursor.fetchone()[0]:
			self.cursor.execute(
				open('sql/create-db-postgres.sql').read()
			)

		self.cursor.execute(
			open('sql/create-table.sql').read()
		)

		self.sql = open('sql/insert.sql').read()

		self.es = Indexer()

	def store(
			self,
			number: int,
			processed: str,
			index: str
	) -> None:
		"""Store data in the Postgres database.

		This method will store (number, processed) in the Postgres database by
		executing the insert SQL script in the client's cursor and committing
		the changes to the database.

		It will also index this 'archived-Postgres' event in ES.

		:param number: Input from Inputter.
		:param processed: Output from Speller.
		:param index: ES index for this 'archived-Mongo' event.

		"""
		self.cursor.execute(
			self.sql, (number, processed)
		)

		self.client.commit()

		self.es.index_record(
			number=number, what='archived-Postgres', index=index
		)
