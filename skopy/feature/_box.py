import uuid

import geoalchemy2
import sqlalchemy
import sqlalchemy_utils

from ._base import Base


class Box(Base):
    __tablename__ = "boxes"

    area = sqlalchemy.Column(sqlalchemy.Integer)

    centroid = geoalchemy2.Geometry("POINT")

    id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), primary_key=True)

    maximum = geoalchemy2.Geometry("POINT")
    minimum = geoalchemy2.Geometry("POINT")

    @staticmethod
    def measure(properties):
        parameters = {
            "area": properties.bbox_area,
            "centroid": "POINT({} {})".format(properties.local_centroid[0], properties.local_centroid[1]),
            "id": uuid.uuid4(),
            "maximum": "POINT({} {})".format(properties.bbox[2], properties.bbox[3]),
            "minimum": "POINT({} {})".format(properties.bbox[0], properties.bbox[1])
        }

        return Box(**parameters)
