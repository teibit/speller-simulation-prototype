"""Observer module.

This file defines the Observer, which can be instantiated on each database
individually by specifying an argument for it in the Dockerfile.

The purpose of the Observer is to observe the target database. It does this by
fetching all the data periodically and displaying it avoiding duplicate
printing. So the UI will display the DB with all its latest additions.

"""
import sys

from time import sleep
from typing import Literal, Union

from retrying import retry

from src.common.databases import Mongo, MySQL, Postgres, Redis

# Store observed data to avoid re-printing it.
observed: list = []


class Observer:
    """Observer class.

    This class defines an Observer initialized on a specific database.

    It allows for the retrieval of all the data in the database periodically,
    with the purpose of displaying all the latest additions.

    """
    # Database client to observe on. These are our custom classes.
    client: Union[
        MySQL,
        Postgres,
        Redis,
        Mongo
    ] = None

    # The retry decorator is helpful for dealing with possible intermittent
    # connection issues. It prevents the container from crashing entirely and
    # thus makes the application more fault-tolerant.
    @retry(wait_fixed=5000, stop_max_attempt_number=12)
    def __init__(self, client_name: str) -> None:
        """Initialize the Observer's client given command-line argument."""
        match client_name:
            case 'MySQL':
                self.client = MySQL()
            case 'Postgres':
                self.client = Postgres()
            case 'Redis':
                self.client = Redis()
            case 'Mongo':
                self.client = Mongo()

    def observe(self):
        """Observe the target database.

        This method will fetch all the data in the target database and display
        the latest updates.

        By making use of the global observed list, this container will keep
        track of all the data it has shown and will avoid showing it again on
        screen. This will create the effect of an updated dashboard.

        """
        for record in self.client.observe():
            # Skip observed records.
            if record in observed:
                continue

            print(record)

            # Consider this record as observed.
            observed.append(record)


def observe(
        client_name: str
) -> None:
    """Observe the target database.

    This method uses an Observer object to peek into the target database.

    It finishes by closing the connection and deleting the Observer. However,
    the state of observed records is preserved in the global list 'observed'.

    :param client_name: The name of the target database.

    """
    observer = Observer(client_name)
    observer.observe()
    observer.client.terminate()

    # Reasonable period to wait before re-peeking for updates.
    sleep(75)


def main() -> None:
    """Main function.

    This script will observe the current state of the target database
    periodically.

    More specifically, it will use Observer objects to retrieve snapshots of
    the target database and display its latest additions.

    The Observer objects are created and destroyed on each iteration,
    simulating different observers peeking into the database over time.

    """
    # The DB client name is specified as a command line argument in the
    # respective Dockerfile (there's one for each name; there's an observer
    # per database).
    client_name: str = sys.argv[1]

    print(f'Beginning observing on {client_name}...\n')

    # After 3 minutes, the databases will begin to show processed records.
    sleep(180)

    # Observe indefinitely.
    while True:
        observe(client_name)


if __name__ == '__main__':
    main()
