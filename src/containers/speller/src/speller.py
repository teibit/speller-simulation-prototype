"""Speller worker.

This script simulates the function of a worker that receives ints via the
Kafka topic Numbers, processes them and produces an output to the separate Kafka
topic Numbers-Processed.

In particular, the processing is the spelling of the ints. The output form is a
tuple of input and output. For example: 0 -> (0, 'zero').

This worker will function indefinitely.

"""
from time import sleep

import inflect

from src.common.utils import consume_int, produce_processed


def speller(number: int) -> str:
    """Speller.

    This function exemplifies the core worker functionality of the Speller
    worker container. It is what processes the input.

    The spelling is done via the inflect module. This function is effectively
    a wrapper around it.

    :param number: input number to be spelled out.

    :return: textual spelling of the input

    """
    return inflect.engine().number_to_words(number)


def spell() -> None:
    """Spell: Receive, process, produce.

    This function will get the input int, process it, and produce the output.

    """
    topic: str = 'Numbers'

    number = consume_int(topic)

    produce_processed(
        message=(number, speller(number)), topic=topic
    )


def main() -> None:
    """Main function.

    This script will do the spelling continuously.

    More specifically, it will consume an int through the Kafka topic Numbers,
    and produce (a tuple containing it and) its spelling through
    Numbers-Processed. The consuming is a blocking call, which spaces out
    spellings over time.

    The Consumer & Producer objects are created and destroyed on each iteration,
    simulating different consumers & producers interacting with the Kafka
    broker.

    """
    print('Beginning the spelling...\n')

    sleep(45)

    while True:
        spell()


if __name__ == '__main__':
    main()
