import uuid

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils

from ._base import Base


class Description(Base):
    __tablename__ = "descriptions"

    image_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(), sqlalchemy.ForeignKey("images.id"))

    keypoint_x = sqlalchemy.Column(sqlalchemy.Float)
    keypoint_y = sqlalchemy.Column(sqlalchemy.Float)

    orientation = sqlalchemy.Column(sqlalchemy.Float)

    response = sqlalchemy.Column(sqlalchemy.Float)

    scale = sqlalchemy.Column(sqlalchemy.Float)

    @staticmethod
    def measure(index, descriptor):
        parameters = {
            "id": uuid.uuid4(),
            "keypoint_x": descriptor.keypoints[index][0],
            "keypoint_y": descriptor.keypoints[index][1],
            "orientation": descriptor.orientations[index],
            "response": descriptor.responses[index],
            "scale": descriptor.scales[index]
        }

        return Description(**parameters)
