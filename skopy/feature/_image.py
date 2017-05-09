import skimage.io
import skimage.measure
import sqlalchemy
import sqlalchemy.orm

from ._base import Base
from ._instance import Instance
from ._intensity import Intensity


class Image(Base):
    __tablename__ = "images"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    instances = sqlalchemy.orm.relationship("Instance", backref="image")

    intensity_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("intensities.id"), nullable=False, unique=True)

    intensity = sqlalchemy.orm.relationship("Intensity", backref=sqlalchemy.orm.backref("image", uselist=False))

    pathname = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __init__(self, pathname, mask):
        self.pathname = pathname

        image = skimage.io.imread(pathname)

        self.intensity = Intensity(image)

        label = skimage.io.imread(mask)

        for properties in skimage.measure.regionprops(label, image):
            instance = Instance(mask, properties)

            self.instances.append(instance)
