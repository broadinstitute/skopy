import celery
import sqlalchemy.orm

import skopy.command
import skopy.feature

queue = celery.Celery("tasks", backend="rpc://", broker="amqp://localhost")

engine = sqlalchemy.create_engine("postgresql+psycopg2://allen@localhost/skopy-test", echo=True)

skopy.feature.Base.metadata.drop_all(engine)

skopy.feature.Base.metadata.create_all(engine)

session = sqlalchemy.orm.sessionmaker()

session.configure(bind=engine)

session = session()


@queue.task
def measure(pathname, mask):
    image = skopy.feature.extract(pathname, mask)

    session.add(image)

    session.commit()
