"""Benchmarker module.

The Benchmarker communicates with ElasticSearch to benchmark the performance
of the system.

In particular, it tracks the completion time of each step of the pipeline,
beginning with inputting (production of the input), following with the spelling
(processing of the input and generation of output), and ending with the
archival of the processed output into each database.

"""
from time import sleep
from datetime import datetime

from typing import Literal, Union

from elasticsearch import Elasticsearch

# Store benchmarked data to avoid reprocessing it.
benchmarked: list = []


class Benchmarker:
    """Benchmarker class.

    This class defines the Benchmarker, hosting an ElasticSearch instance and
    providing methods for benchmarking the performance of the system.

    """
    topic: str = None

    es: Elasticsearch = None
    es_search: list = None
    es_numbers: list = None

    def __init__(
            self, topic: str
    ) -> None:
        """Initialize the Benchmarker object.

        An associated ElasticSearch instance is also initialized, along with
        some pre-fetched ElasticSearch data relevant to the topic.

        """
        self.topic = topic

        # Get an Elasticsearch client with basic defaults.
        self.es = Elasticsearch(
            hosts='https://localhost:9200',
            basic_auth=('elastic', 'elastic'),
            verify_certs=False  # for simplicity
        )

        # Get all documents on the index.
        self.es_search = self.es.search(
            index=self.topic.lower(),
            body={"query": {"match_all": {}}, "size": 5000}
        )['hits']['hits']

        # Get all numbers (app's inputs by Inputter) from the documents.
        self.es_numbers = list(set(
          [record['_source']['Number'] for record in self.es_search]
        ))

    def _get_timestamp(
            self,
            number: int,
            what: Literal[
                'produced',
                'processed',
                'archived-MySQL',
                'archived-Postgres',
                'archived-Redis',
                'archived-Mongo'
            ]
    ) -> Union[
        float, None
    ]:
        """Get a timestamp from the record of a number.

        This is an internal helper method that will retrieve the timestamp
        of an event that was recorded as a number flowed through the pipeline.

        It returns None if no such timestamp was found, which may be the case if
        checked ahead of time, i.e. before the event gets to occur.

        """
        record = [
            record['_source']['When']
            for record in self.es_search
            if record['_source']['Number'] == number
               and record['_source']['What'] == what
        ]

        return record[0] if record else None

    def benchmark(self):
        """Do the benchmarking for all available completed payloads.

        This method will compute performance statistics for all records that
        have completed all steps of the pipeline successfully.

        It will then print those statistics to stdout, making sure to avoid
        re-printing of already-benchmarked records.

        """
        # Begin benchmarking on all numbers on the topic.
        for number in self.es_numbers:
            produced_timestamp = self._get_timestamp(
                number=number, what='produced'
            )

            # Skip record if already benchmarked.
            if (number, produced_timestamp) in benchmarked:
                continue

            processed_timestamp = self._get_timestamp(
                number=number, what='processed'
            )

            # Get timestamp of database archivals.
            archived_mysql_timestamp = self._get_timestamp(
                number=number, what='archived-MySQL'
            )
            archived_postgres_timestamp = self._get_timestamp(
                number=number, what='archived-Postgres'
            )
            archived_redis_timestamp = self._get_timestamp(
                number=number, what='archived-Redis'
            )
            archived_mongo_timestamp = self._get_timestamp(
                number=number, what='archived-Mongo'
            )

            # Skip this record if any timestamp is missing.
            if (
                    not produced_timestamp or
                    not processed_timestamp or
                    not archived_mysql_timestamp or
                    not archived_postgres_timestamp or
                    not archived_redis_timestamp or
                    not archived_mongo_timestamp
            ):
                continue

            # Calculate the time it takes the records to be processed.
            processing_time = processed_timestamp - produced_timestamp

            # Calculate the time it takes the processed records to be archived.
            mysql_archiving_time = (
                archived_mysql_timestamp - processed_timestamp
            )
            postgres_archiving_time = (
                archived_postgres_timestamp - processed_timestamp
            )
            redis_archiving_time = (
                archived_redis_timestamp - processed_timestamp
            )
            mongo_archiving_time = (
                archived_mongo_timestamp - processed_timestamp
            )

            # Calculate the total time of the processing of a record,
            # beginning with inputting and finishing with archiving on each db.
            mysql_total_time = processing_time + mysql_archiving_time
            postgres_total_time = processing_time + postgres_archiving_time
            redis_total_time = processing_time + redis_archiving_time
            mongo_total_time = processing_time + mongo_archiving_time

            # Print out all statistics nicely.
            print(
                f'Number: {number}\n\n'
                
                f'Produced: {datetime.fromtimestamp(produced_timestamp)}\t'
                f'Processing time: {round(processing_time, 2)}\n\n'
                
                f'MySQL\t'
                f'Archiving time: {round(mysql_archiving_time, 2)}\t'
                f'Total time: {round(mysql_total_time, 2)}\n'
                
                f'Postgres\t'
                f'Archiving time: {round(postgres_archiving_time, 2)}\t'
                f'Total time: {round(postgres_total_time, 2)}\n'
                
                f'Redis\t'
                f'Archiving time: {round(redis_archiving_time, 2)}\t'
                f'Total time: {round(redis_total_time, 2)}\n'

                f'Mongo\t'
                f'Archiving time: {round(mongo_archiving_time, 2)}\t'
                f'Total time: {round(mongo_total_time, 2)}\n\n'
            )

            # Store benchmarked record to avoid re-benchmarking.
            benchmarked.append((number, produced_timestamp))


def benchmark() -> None:
    """Benchmark the flow of the inputs across the pipeline.

    This method uses a Benchmarker object to gather statistics about the
    performance of the system.

    It finishes by closing the connection to the ElasticSearch server. However,
    the state of benchmarked inputs is preserved in the global list
    'benchmarked'.

    """
    topic: str = 'Numbers'

    benchmarker = Benchmarker(topic)

    benchmarker.benchmark()

    benchmarker.es.close()

    # In a minute there should already be more inputs fully processed through
    # the pipeline ready to be benchmarked.
    sleep(60)


def main():
    """Main function.

    This script will benchmark the completion time of each step of the pipeline.

    More specifically, it will use Benchmarker objects to calculate the time
    it takes for each step of the pipeline to be completed.

    The Benchmarker objects are created and destroyed on each iteration,
    simulating different ElasticSearch workers coming in over time.

    """
    print(f'Beginning benchmarking...\n')

    # After 3 minutes, some inputs should have already been processed and
    # archived, so then is when the benchmarking actually starts.
    sleep(180)

    # Benchmark indefinitely.
    while True:
        benchmark()


if __name__ == '__main__':
    main()
