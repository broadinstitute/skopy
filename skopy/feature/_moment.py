import enum

import sqlalchemy

from ._base import Base


class MomentType(enum.Enum):
    central = 1

    normalized = 2

    spatial = 3

    zernike = 4


class Moment(Base):
    __tablename__ = "moments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    instance_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("instances.id"))

    description = sqlalchemy.Column(sqlalchemy.Enum(MomentType))

    weighted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    p = sqlalchemy.Column(sqlalchemy.Integer)
    q = sqlalchemy.Column(sqlalchemy.Integer)

    y = sqlalchemy.Column(sqlalchemy.Float)

    def __init__(self, description, p, q, y, weighted=False):
        self.description = description

        self.weighted = weighted

        self.p = p
        self.q = q

        self.y = y
