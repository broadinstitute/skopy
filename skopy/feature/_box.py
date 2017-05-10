# -*- coding: utf-8 -*-

import uuid

import sqlalchemy

from ._base import Base


class Box(Base):
    __tablename__ = "boxes"

    area = sqlalchemy.Column(sqlalchemy.Integer)

    centroid_x = sqlalchemy.Column(sqlalchemy.Integer)
    centroid_y = sqlalchemy.Column(sqlalchemy.Integer)

    maximum_x = sqlalchemy.Column(sqlalchemy.Integer)
    maximum_y = sqlalchemy.Column(sqlalchemy.Integer)

    minimum_x = sqlalchemy.Column(sqlalchemy.Integer)
    minimum_y = sqlalchemy.Column(sqlalchemy.Integer)

    @staticmethod
    def measure(properties):
        parameters = {
            "area": properties.bbox_area,
            "centroid_x": properties.local_centroid[0],
            "centroid_y": properties.local_centroid[1],
            "id": uuid.uuid4(),
            "maximum_x": properties.bbox[2],
            "maximum_y": properties.bbox[3],
            "minimum_x": properties.bbox[0],
            "minimum_y": properties.bbox[1],
        }

        return Box(**parameters)
