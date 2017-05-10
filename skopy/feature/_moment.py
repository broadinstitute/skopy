# -*- coding: utf-8 -*-

import enum
import uuid

import numpy
import sqlalchemy
import sqlalchemy_utils

from ._base import Base


class MomentType(enum.Enum):
    central = 1

    inertia = 2

    normalized = 3

    spatial = 4

    zernike = 5


class Moment(Base):
    __tablename__ = "moments"

    description = sqlalchemy.Column(sqlalchemy.Enum(MomentType))

    instance_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(), sqlalchemy.ForeignKey("instances.id"))

    p = sqlalchemy.Column(sqlalchemy.Integer)
    q = sqlalchemy.Column(sqlalchemy.Integer)

    weighted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    y = sqlalchemy.Column(sqlalchemy.Float)

    @staticmethod
    def measure(description, p, q, moments, weighted):
        if description is MomentType.zernike:
            y = 0 if numpy.isnan(moments[p + 1][q] ) else moments[p + 1][q]
        else:
            y = 0 if numpy.isnan(moments[p, q]) else moments[p, q]

        parameters = {
            "description": description,
            "id": uuid.uuid4(),
            "p": p + 1,
            "q": q + 1,
            "weighted": weighted,
            "y": y
        }

        return Moment(**parameters)
