# Speller simulation prototype

## Background

This repository contains a minimal yet modern prototype of a simple simulation.

This project shines at integrating several state-of-the-art software technologies in a cohesive and practically plausible way. It exists merely to show what's possible, and thus is fundamentally limited in practical usefulness. Nevertheless, it's a beautiful possible blueprint for significantly more complex systems.

With this public repository, I hope to inspire others and even myself to create more elaborate similar systems.

## System overview

This prototype is, at its core, a distributed system of microservices that work together while remaining independent entities.

The simulation works by the deliberate collaboration between independent nodes that run simultaneously in a way that is coordinated in time. It therefore creates a pipeline whereby each node separately performs a concrete action on it.

### Core technologies

A careful selection of state-of-the-art software technologies make this simulation possible. The following is a description of those core components of this application's tech stack:

1. [Python](https://www.python.org/): this application is built entirely in Python 3 (latest version). Many of the technologies presented below are a part of this project thanks to the existance of Python connector modules developed to integrate Python with them.
2. [Docker](https://www.docker.com/): the leader containerization software on the market. The microservices of this application are Docker containers. They're entirely independent entities that end up collaborating seamlessly together. This prototype presents a series of modules and those are run as Docker containers, but also ready-made images from [Docker Hub](https://hub.docker.com/) are run as containers too.
3. [Kubernetes](https://kubernetes.io/): Kubernetes is the leading open-source container orchestration system of today. Each module of this app runs on its own independent container, and Kubernetes coordinates their deployment. By means of a manifest (Kubernetes YAML), the containers are ignited from their corresponding images, volumes are set to persist data during the simulation, and policies customizing the deployment are established. Kubernetes is what ensures that the simulation runs as expected over time, providing a highly scalable and fault-tolerant platform for directing the microservices. This app relies on the convenient integration between Docker and Kubernetes via [Docker Desktop](https://www.docker.com/products/docker-desktop/).
4. [Kafka](https://kafka.apache.org/): Apache Kafka is at the foundation of this simulation. It is the leading open-source message streaming platform of the modern day. This app uses the Docker image [bitnami/kafka](https://hub.docker.com/r/bitnami/kafka) and the modern Python connector [kafka-python-ng](https://pypi.org/project/kafka-python-ng/). Kafka works by hosting a broker with wich producers and consumers and interact via topics. In this application, inputs get to the speller via the topic Numbers, and processed outputs get to the archiver via the topic Numbers-Processed. Custom Consumer & Producer classes are presented to handle such operations.
4. [MySQL](https://www.mysql.com/): MySQL is an extremely popular SQL database management system. This app uses the Docker image [mysql](https://hub.docker.com/_/mysql) and the Python connector [mysql-connector-python](https://pypi.org/project/mysql-connector-python/). A standard relational table of columns Number & Spelling store the results of this simulation.
5. [Postgres](https://www.postgresql.org/): Postgres is portrayed as an advanced open-source SQL database management system. In this application, it stores data just like MySQL, and is used as an alternative SQL system.  This app uses the Docker image [postgres](https://hub.docker.com/_/postgres) and the Python connector [psycopg2-binary](https://pypi.org/project/psycopg2-binary/).
6. [Redis](https://redis.io/): Redis is a fast in-memory No-SQL database that is widely used. In this application, data is stored in the form of key-value pairs, where key is the number input and value is the processed output (the spelling of the number). Redis therefore serves as an in-memory dictionary of records, providing superb performance. This app uses the Docker image [redis](https://hub.docker.com/_/redis) and the Python connector [redis](https://pypi.org/project/redis/).
7. [MongoDB](https://www.mongodb.com/): MongoDB is a leading No-SQL database management platform based on documents, which are simple JSON-like dictionary structures. It is also very fast, and this application uses it in a similar way as Redis, but the documents follow the structure `{'Number': number, 'Spelling': processed}`. This app uses the Docker image [mongo](https://hub.docker.com/_/mongo) and the Python connector [pymongo](https://pypi.org/project/pymongo/).
8. [Elasticsearch](https://www.elastic.co/Elasticsearch): Elasticsearch is the leading distributed analytics platform. It serves the very important role in this application of tracking the completion of each step of the pipeline on each input, thereby providing a way to measure the performance of the simulation. This app uses the Docker image [Elasticsearch](https://hub.docker.com/_/Elasticsearch) and the Python connector [Elasticsearch](https://pypi.org/project/Elasticsearch/).

### Pipeline

The simulation runs the following time-coordinated steps:

1. Servers start.
   1. **Kubernetes**: Orchestrator that ensures the simulation runs.
   2. **Kafka**: Provides a broker for pipelining messages across the system.
   2. **MySQL**: SQL DB.
   3. **Postgres**: SQL DB.
   4. **Redis**: No-SQL DB.
   5. **Mongo**: No-SQL DB.
   6. **Elasticsearch**: Track performance of events through the pipeline.
2. Clients start.
   1. **Inputter**: Sends input messages to the system to be processed across the pipeline.
   2. **Speller**: Main worker of the system. It is what processes the input and produces an output.
   3. **Archivers**: Archive processed messages into their corresponding database.
   4. **Observers**: Show entire database including latest additions.
   5. **Benchmarker**: Shows performance statistics for every message sent through the pipeline.

Initially, all servers start up. Then the inputter begins sending integers to the Kafka topic Numbers and then logging these 'produced' events in Elasticsearch documents including the timestamp. These messages are received and managed by the Kafka broker.

Then the Speller module picks up those messages from Numbers, generates their spelling, and produces a tuple containing `(Number, Spelling)` to the separate Kafka topic Numbers-Processed. It likewise logs these 'processed' events.

Finally, the Archiver modules pick up those messages from Numbers-Processed and store them into all DBs. It likewise logs these 'archived-db' events.

The Observer modules will then begin displaying the current state of the databases in a dashboard-like fashion since it continues to display new records as they become available.

The Benchmarker module will communicate the Elasticsearch server and compute the time it takes the inputs to complete each step of the pipeline: beginning with production, following with processing and ending with archival in a database. It will continue to benchmark new records as they become available.
