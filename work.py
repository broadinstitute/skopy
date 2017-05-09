import celery

broker = celery.Celery("tasks", backend="rpc://", broker="amqp://localhost")


@broker.task
def add(x, y):
    return x + y
