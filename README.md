# skopy

```sh
$ skopy measure skopy/data/metadata.csv
```

## Installation

```sh
$ pip install --editable .
```

## Storage

Skopy extracts features to a SQLite database by default. You can use a different database by passing the ``--database`` flag with a connection URL for your Microsoft SQL Server, MySQL, PostgreSQL, Oracle, or SQLite database.

## Task queue

A task queue is a mechanism to distribute work (e.g. feature extraction) across threads or machines. A task queue’s unit of work is a task. One, or many, dedicated worker processes monitor Skopy’s task queue for new work to perform.

Skopy uses a message broker to mediate between clients and workers. To initiate a task the client adds a message to the queue, the broker then delivers that message to a worker. A Skopy installation can consist of multiple workers and message brokers to facilitate high availability and horizontal scaling.

Skopy can run on a single machine, on multiple machines, or even across data centers.

### Prerequisites

Skopy requires a message broker to send and receive messages.

There’re four choices:

#### RabbitMQ

RabbitMQ is feature-complete, stable, durable and easy to install. It’s an excellent choice for a production environment.

#### Redis

Redis is feature-complete, but is susceptible to data loss in the event of abrupt termination or power failures.

#### Amazon Simple Queue Service (SQS)

#### Apache ZooKeeper

### Use

You can run the worker by executing the following:

```sh
$ celery -A skopy.task worker --loglevel=info
```

In production you’ll want to run the worker in the background as a daemon. To do this you need to use the tools provided by your platform, or something like [supervisord](http://supervisord.org/) (see [Daemonization](http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#daemonizing) for more information).

For a complete listing of the command-line options available, try:

```sh
$  celery worker --help
```
