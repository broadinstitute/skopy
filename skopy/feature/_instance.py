import uuid

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils

from ._base import Base


class Instance(Base):
    __tablename__ = "instances"

    box_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(), sqlalchemy.ForeignKey("boxes.id"))
    box = sqlalchemy.orm.relationship("Box", backref=sqlalchemy.orm.backref("instance", uselist=False))

    centroid_x = sqlalchemy.Column(sqlalchemy.Integer)
    centroid_y = sqlalchemy.Column(sqlalchemy.Integer)

    image_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(), sqlalchemy.ForeignKey("images.id"))

    index = sqlalchemy.Column(sqlalchemy.Integer)

    intensity_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(), sqlalchemy.ForeignKey("intensities.id"))
    intensity = sqlalchemy.orm.relationship("Intensity", backref=sqlalchemy.orm.backref("instance", uselist=False))

    moments = sqlalchemy.orm.relationship("Moment", backref="instance")

    shape_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(), sqlalchemy.ForeignKey("shapes.id"))
    shape = sqlalchemy.orm.relationship("Shape", backref=sqlalchemy.orm.backref("instance", uselist=False))

    @staticmethod
    def measure(properties):
        parameters = {
            "centroid_x": properties.centroid[0],
            "centroid_y": properties.centroid[1],
            "id": uuid.uuid4(),
            "index": properties.label,
        }

        return Instance(**parameters)
