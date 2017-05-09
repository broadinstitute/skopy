import sqlalchemy

from ._base import Base


class Box(Base):
    __tablename__ = "boxes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    area = sqlalchemy.Column(sqlalchemy.Integer)

    minimum_x = sqlalchemy.Column(sqlalchemy.Integer)
    minimum_y = sqlalchemy.Column(sqlalchemy.Integer)

    maximum_x = sqlalchemy.Column(sqlalchemy.Integer)
    maximum_y = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, properties):
        self.area = properties.bbox_area

        self.minimum_x = properties.bbox[0]
        self.minimum_y = properties.bbox[1]

        self.maximum_x = properties.bbox[2]
        self.maximum_y = properties.bbox[3]
