"""Utilities module.

This module contains common utilities used throughout the entire application.

It abstracts away some of the complex functionality behind the app's
functioning.

"""
import pickle

from typing import Literal, Tuple

from src.common.producer import Producer
from src.common.consumer import Consumer


def produce_processed(
        message: Tuple[int, str],
        topic: Literal['Numbers']
) -> None:
    """Produce a processed int to the corresponding topic.

    This function uses a Producer to produce the given message to the
    Processed topic related to the given topic.

    :param message: Tuple of the form (input, output).
    :param topic: Kafka topic associated with the input int.

    """
    # Get a Producer object that communicates with localhost:9092.
    producer = Producer(
        value_serializer=lambda x: pickle.dumps(x)
    )

    print(f'Processing and producing to broker via {topic}-Processed...')

    # Produce the message to its -Processed related topic.
    producer.produce(
        data=message,
        topic=topic + '-Processed',
        index=topic.lower(),
        what='processed',
    )

    print()

    # Close Kafka producer (and related Elasticsearch client).
    producer.terminate()


def consume_int(
    topic: Literal['Numbers']
) -> int:
    """Consume an int from an input topic.

    This function uses a Consumer to consume an int from the given input topic.

    :param topic: Topic to consume ints from.

    :return: consumed int

    """
    # Get a fresh Consumer on the given topic.
    consumer = Consumer(
        topic=topic,
        group_id='processors',
        value_deserializer=lambda x: int.from_bytes(x, 'big')
    )

    # Consume a message on this topic. This is a blocking call.
    message = consumer.consume()

    # Notice that this is a parent class method.
    consumer.close()

    return message.value


def consume_processed(
    topic: str
) -> Tuple[int, str]:
    """Consume an output tuple from a Processed topic.

    This function uses a Consumer to consume a tuple of the form (input,
    output) from the given input topic.

    :param topic: Topic to consume tuples from.

    :return: consumed tuple

    """
    # Get a fresh Consumer on the given topic.
    consumer = Consumer(
        topic=topic + '-Processed',
        group_id='archiver',
        value_deserializer=lambda x: pickle.loads(x)
    )

    # Consume a message on this topic. This is a blocking call.
    message = consumer.consume()

    # Notice that this is a parent class method.
    consumer.close()

    return message
