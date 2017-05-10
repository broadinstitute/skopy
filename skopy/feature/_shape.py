import uuid

import sqlalchemy
import sqlalchemy_utils

from ._base import Base


class Shape(Base):
    __tablename__ = "shapes"

    area = sqlalchemy.Column(sqlalchemy.Float)

    axis_major = sqlalchemy.Column(sqlalchemy.Float)
    axis_minor = sqlalchemy.Column(sqlalchemy.Float)

    eccentricity = sqlalchemy.Column(sqlalchemy.Float)

    equivalent_diameter = sqlalchemy.Column(sqlalchemy.Float)

    euler_number = sqlalchemy.Column(sqlalchemy.Integer)

    extent = sqlalchemy.Column(sqlalchemy.Float)

    id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), primary_key=True)

    orientation = sqlalchemy.Column(sqlalchemy.Float)

    perimeter = sqlalchemy.Column(sqlalchemy.Float)

    solidity = sqlalchemy.Column(sqlalchemy.Float)

    @staticmethod
    def measure(properties):
        parameters = {
            "area": properties.area,
            "axis_major": properties.major_axis_length,
            "axis_minor": properties.minor_axis_length,
            "eccentricity": properties.eccentricity,
            "equivalent_diameter": properties.equivalent_diameter,
            "euler_number": properties.euler_number,
            "extent": properties.extent,
            "id": uuid.uuid4(),
            "orientation": properties.orientation,
            "perimeter": properties.perimeter,
            "solidity": properties.solidity
        }

        return Shape(**parameters)
