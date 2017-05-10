import sqlalchemy
import sqlalchemy_utils
import uuid
from ._base import Base


class Box(Base):
    __tablename__ = "boxes"

    area = sqlalchemy.Column(sqlalchemy.Integer)

    id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), primary_key=True)

    maximum_x = sqlalchemy.Column(sqlalchemy.Integer)
    maximum_y = sqlalchemy.Column(sqlalchemy.Integer)

    minimum_x = sqlalchemy.Column(sqlalchemy.Integer)
    minimum_y = sqlalchemy.Column(sqlalchemy.Integer)

    @staticmethod
    def measure(properties):
        parameters = {
            "area": properties.bbox_area,
            "id": uuid.uuid4(),
            "maximum_x": properties.bbox[2],
            "maximum_y": properties.bbox[3],
            "minimum_x": properties.bbox[0],
            "minimum_y": properties.bbox[1]
        }

        return Box(**parameters)
