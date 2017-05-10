import uuid

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils

from ._base import Base


class Image(Base):
    __tablename__ = "images"

    instances = sqlalchemy.orm.relationship("Instance", backref="image")

    intensity_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), sqlalchemy.ForeignKey("intensities.id"))
    intensity = sqlalchemy.orm.relationship("Intensity", backref=sqlalchemy.orm.backref("image", uselist=False))

    pathname = sqlalchemy.Column(sqlalchemy.String)

    @staticmethod
    def measure(pathname):
        parameters = {
            "id": uuid.uuid4(),
            "pathname": pathname
        }

        return Image(**parameters)
