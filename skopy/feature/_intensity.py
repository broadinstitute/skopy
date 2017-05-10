import uuid

import numpy
import sqlalchemy

from ._base import Base


class Intensity(Base):
    __tablename__ = "intensities"

    integrated = sqlalchemy.Column(sqlalchemy.Float)

    maximum = sqlalchemy.Column(sqlalchemy.Float)

    mean = sqlalchemy.Column(sqlalchemy.Float)

    median = sqlalchemy.Column(sqlalchemy.Float)

    median_absolute_deviation = sqlalchemy.Column(sqlalchemy.Float)

    minimum = sqlalchemy.Column(sqlalchemy.Float)

    quartile_1 = sqlalchemy.Column(sqlalchemy.Float)

    quartile_2 = sqlalchemy.Column(sqlalchemy.Float)

    quartile_3 = sqlalchemy.Column(sqlalchemy.Float)

    standard_deviation = sqlalchemy.Column(sqlalchemy.Float)

    @staticmethod
    def measure(image):
        properties = {
            "id": uuid.uuid4(),
            "integrated": numpy.sum(image),
            "maximum": numpy.max(image),
            "mean": numpy.mean(image),
            "median": numpy.median(image),
            "median_absolute_deviation": numpy.median(numpy.abs(numpy.ma.array(image).compressed() - numpy.median(image))),
            "minimum": numpy.min(image),
            "quartile_1": numpy.percentile(image, 25),
            "quartile_2": numpy.percentile(image, 50),
            "quartile_3": numpy.percentile(image, 75),
            "standard_deviation": numpy.std(image)
        }

        return Intensity(**properties)
