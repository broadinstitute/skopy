import enum
import uuid

import numpy
import sqlalchemy
from sqlalchemy_utils import UUIDType

from ._base import Base


class MomentType(enum.Enum):
    central = 1

    normalized = 2

    spatial = 3

    zernike = 4


class Moment(Base):
    __tablename__ = "moments"

    description = sqlalchemy.Column(sqlalchemy.Enum(MomentType))

    id = sqlalchemy.Column(UUIDType(binary=False), primary_key=True)

    instance_id = sqlalchemy.Column(UUIDType(binary=False), sqlalchemy.ForeignKey("instances.id"))

    p = sqlalchemy.Column(sqlalchemy.Integer)
    q = sqlalchemy.Column(sqlalchemy.Integer)

    weighted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    y = sqlalchemy.Column(sqlalchemy.Float)

    @staticmethod
    def measure(description, p, q, moments, weighted):
        parameters = {
            "description": description,
            "id": uuid.uuid4(),
            "p": p + 1,
            "q": q + 1,
            "weighted": weighted,
            "y": 0 if numpy.isnan(moments[p, q]) else moments[p, q]
        }

        return Moment(**parameters)
