import uuid

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils

from ._base import Base


class Instance(Base):
    __tablename__ = "instances"

    box_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), sqlalchemy.ForeignKey("boxes.id"))
    box = sqlalchemy.orm.relationship("Box", backref=sqlalchemy.orm.backref("instance", uselist=False))

    centroid_weighted_local_x = sqlalchemy.Column(sqlalchemy.Float)
    centroid_weighted_local_y = sqlalchemy.Column(sqlalchemy.Float)

    centroid_weighted_x = sqlalchemy.Column(sqlalchemy.Float)
    centroid_weighted_y = sqlalchemy.Column(sqlalchemy.Float)

    centroid_x = sqlalchemy.Column(sqlalchemy.Float)
    centroid_y = sqlalchemy.Column(sqlalchemy.Float)

    id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), primary_key=True)

    image_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), sqlalchemy.ForeignKey("images.id"))

    index = sqlalchemy.Column(sqlalchemy.Integer)

    inertia_tensor_1_1 = sqlalchemy.Column(sqlalchemy.Float)
    inertia_tensor_1_2 = sqlalchemy.Column(sqlalchemy.Float)
    inertia_tensor_2_1 = sqlalchemy.Column(sqlalchemy.Float)
    inertia_tensor_2_2 = sqlalchemy.Column(sqlalchemy.Float)

    inertia_tensor_eigvals_1 = sqlalchemy.Column(sqlalchemy.Float)
    inertia_tensor_eigvals_2 = sqlalchemy.Column(sqlalchemy.Float)

    intensity_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), sqlalchemy.ForeignKey("intensities.id"))
    intensity = sqlalchemy.orm.relationship("Intensity", backref=sqlalchemy.orm.backref("instance", uselist=False))

    moments = sqlalchemy.orm.relationship("Moment", backref="instance")

    pathname = sqlalchemy.Column(sqlalchemy.String)

    shannon_entropy = sqlalchemy.Column(sqlalchemy.Float)

    shape_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), sqlalchemy.ForeignKey("shapes.id"))
    shape = sqlalchemy.orm.relationship("Shape", backref=sqlalchemy.orm.backref("instance", uselist=False))

    @staticmethod
    def measure(properties):
        parameters = {
            "centroid_weighted_local_x": properties.weighted_local_centroid[0],
            "centroid_weighted_local_y": properties.weighted_local_centroid[1],
            "centroid_weighted_x": properties.weighted_centroid[0],
            "centroid_weighted_y": properties.weighted_centroid[1],
            "centroid_x": properties.centroid[0],
            "centroid_y": properties.centroid[1],
            "id": uuid.uuid4(),
            "index": properties.label,
            "inertia_tensor_1_1": properties.inertia_tensor[0, 0],
            "inertia_tensor_1_2": properties.inertia_tensor[0, 1],
            "inertia_tensor_2_1": properties.inertia_tensor[1, 0],
            "inertia_tensor_2_2": properties.inertia_tensor[1, 1],
            "inertia_tensor_eigvals_1": properties.inertia_tensor_eigvals[0],
            "inertia_tensor_eigvals_2": properties.inertia_tensor_eigvals[1],
        }

        return Instance(**parameters)
