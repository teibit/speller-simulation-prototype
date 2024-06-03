import contextlib
from multiprocessing import Process

from time import sleep

from retrying import retry

from src.common.databases import Mongo, MySQL, Postgres, Redis
from src.common.utils import consume_processed


class Archiver:
    @retry(wait_fixed=5000, stop_max_attempt_number=12)
    def __init__(self, topic: str) -> None:
        self.topic = topic

        self.MySQL = MySQL()
        self.Postgres = Postgres()
        self.Redis = Redis()
        self.Mongo = Mongo()

    def archive(self, number: int, processed: str, index: str) -> None:
        print(f'Archiving processed message into DBs...')

        db_storers = []

        for target in [
            self.MySQL.store,
            self.Postgres.store,
            self.Redis.store,
            self.Mongo.store
        ]:
            db_storers.append(
                Process(
                    target=target, args=(number, processed, index)
                )
            )

        with contextlib.redirect_stdout(None):
            for storer in db_storers:
                storer.start()

        for storer in db_storers:
            storer.join()

    def terminate(self) -> None:
        archiver_terminators = []

        for terminator in [
            self.MySQL.terminate,
            self.Postgres.terminate,
            self.Redis.terminate,
            self.Mongo.terminate
        ]:
            archiver_terminators.append(
                Process(target=terminator)
            )

        for terminator in archiver_terminators:
            terminator.start()

        for terminator in archiver_terminators:
            terminator.join()


def archive() -> None:
    topic: str = 'Numbers'

    record = consume_processed(topic)

    archiver = Archiver(topic)

    archiver.archive(
        number=record.value[0],
        processed=record.value[1],
        index=topic.lower()
    )

    archiver.terminate()

    print()


def main():
    print(f'Beginning archiving...\n')

    sleep(120)

    while True:
        archive()


if __name__ == '__main__':
    main()
