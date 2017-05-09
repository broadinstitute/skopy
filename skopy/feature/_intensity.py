import numpy
import sqlalchemy

from ._base import Base


class Intensity(Base):
    __tablename__ = "intensities"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

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

    def __init__(self, image):
        self.integrated = numpy.sum(image)

        self.maximum = numpy.max(image)

        self.mean = numpy.mean(image)

        self.median = numpy.median(image)

        self.median_absolute_deviation = numpy.median(numpy.abs(numpy.ma.array(image).compressed() - numpy.median(image)))

        self.minimum = numpy.min(image)

        self.quartile_1 = numpy.percentile(image, 25)

        self.quartile_2 = numpy.percentile(image, 50)

        self.quartile_3 = numpy.percentile(image, 75)

        self.standard_deviation = numpy.std(image)

