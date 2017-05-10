import celery.bin
import celery.bootsteps
import sqlalchemy.orm

import skopy.command
import skopy.feature

application = celery.Celery("tasks", backend="rpc://", broker="amqp://localhost")


class Task(celery.Task):
    def __init__(self):
        self.database = "postgresql+psycopg2://allen@localhost/skopy-test"

        self.echo = False

        self._session = None

    @property
    def session(self):
        if self._session is None:
            engine = sqlalchemy.create_engine(self.database, echo=self.echo)

            skopy.feature.Base.metadata.drop_all(engine)

            skopy.feature.Base.metadata.create_all(engine)

            session = sqlalchemy.orm.sessionmaker()

            session.configure(bind=engine)

            self._session = session()

        return self._session

    def run(self, *args, **kwargs):
        super(Task, self).run(*args, **kwargs)


application.user_options["worker"].add(celery.bin.Option("--database", dest="database", default=None))

application.user_options["worker"].add(celery.bin.Option("--echo", dest="echo", default=False))


class Step(celery.bootsteps.Step):
    def __init__(self, parent, database, echo, **kwargs):
        Task.database = database

        Task.echo = echo

        super(Step, self).__init__(parent, **kwargs)

application.steps["worker"].add(Step)


@application.task(base=Task, bind=True)
def measure(self, pathname, mask):
    image = skopy.feature.extract(pathname, mask)

    self.session.add(image)

    self.session.commit()
