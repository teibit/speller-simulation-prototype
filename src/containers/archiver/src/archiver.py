"""Archiver module.

This file defines the Archiver, which archives into all databases the
processed messages.

The Archiver hosts instances of our custom database classes and concurrently
stores the messages it polls in all databases.

"""
import sys

from time import sleep

from retrying import retry

from src.common.databases import Mongo, MySQL, Postgres, Redis
from src.common.utils import consume_processed


class Archiver:
    """Archiver class.

    This class defines an Archiver initialized on a specific database.

    It allows for the archival of messages coming in through a Processed
    Kafka topic into the target database.

    """
    # The retry decorator is helpful for dealing with possible intermittent
    # connection issues. It prevents the container from crashing entirely and
    # thus makes the application more fault-tolerant.
    @retry(wait_fixed=5000, stop_max_attempt_number=12)
    def __init__(
            self, client_name: str
    ) -> None:
        """Initialize the Archiver's client given command-line argument."""
        match client_name:
            case 'MySQL':
                self.client = MySQL()
            case 'Postgres':
                self.client = Postgres()
            case 'Redis':
                self.client = Redis()
            case 'Mongo':
                self.client = Mongo()

    def archive(
            self,
            number: int,
            processed: str,
            index: str
    ) -> None:
        """Archive a message.

        This method will store a processed message in the target database by
        using the .store() method from the Database-derived client.

        """
        print(f'Archiving processed message into DB...')

        self.client.store(
            number, processed, index
        )


def archive(
        client_name: str
) -> None:
    """Archive Processed messages into DB.

    This method uses an Archiver object to store consumed messages into the
    target database.

    It finishes by closing the connection and terminating the Archiver's DB
    client, which also closes the ElasticSearch connection on the background.

    :param client_name: The name of the target database.

    """
    # There's only 1 topic on this simulation for simplicity.
    topic: str = 'Numbers'

    # Consume a Processed Number record. Note that this is a blocking call.
    record = consume_processed(topic)

    archiver = Archiver(client_name)

    archiver.archive(
        number=record.value[0],
        processed=record.value[1],
        index=topic.lower()
    )

    archiver.client.terminate()

    print()


def main() -> None:
    """Main function.

    This script will archive processed messages into the target database
    periodically.

    More specifically, it will use Archiver objects containing a database
    client to archive messages into them after consuming them from the
    Processed topic.

    The Archiver objects are created and destroyed on each iteration,
    simulating different Archiver sending payload to the database over time.

    """
    # The DB client name is specified as a command line argument in the
    # respective Dockerfile (there's one for each name; there's an observer
    # per database).
    client_name: str = sys.argv[1]

    print(f'Beginning archiving on {client_name}...\n')

    # After 2 minutes there should already be some Processed messages ready to
    # be archived.
    sleep(120)

    while True:
        archive(client_name)


if __name__ == '__main__':
    main()
