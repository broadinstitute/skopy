import sqlalchemy.exc
import sqlalchemy.orm.exc

from ._base import Base
from ._correlation import Correlation
from ._image import Image


def find_or_create_by(session, model, method="", parameters=None, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except sqlalchemy.orm.exc.NoResultFound:
        kwargs.update(parameters or {})

        created = getattr(model, method, model)(**kwargs)

        try:
            session.add(created)

            session.commit()

            return created, False
        except sqlalchemy.exc.IntegrityError:
            session.rollback()

            return session.query(model).filter_by(**kwargs).one(), True
