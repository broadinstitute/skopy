# -*- coding: utf-8 -*-

import itertools
import uuid

import celery
import mahotas.features
import numpy
import psycopg2.extensions
import skimage.io
import skimage.measure
import sqlalchemy
import sqlalchemy.orm

import skopy.command
import skopy.feature


psycopg2.extensions.register_adapter(numpy.float64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.uint64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.uint8, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.int64, psycopg2.extensions.AsIs)

broker = celery.Celery("tasks", backend="rpc://", broker="amqp://localhost")


class Session(celery.Task):
    def __init__(self):
        self._engine = sqlalchemy.create_engine("postgresql+psycopg2://allen@localhost/skopy-test", echo=True)

        skopy.feature.Base.metadata.drop_all(self._engine)

        skopy.feature.Base.metadata.create_all(self._engine)

        self._session = None

    def after_return(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

    @property
    def session(self):
        if self._session is None:
            session_maker = sqlalchemy.orm.sessionmaker()

            session_maker.configure(bind=self._engine)

            self._session = session_maker()

        return self._session


@broker.task(base=Session, bind=True)
def measure(self, x, y):
    x_data = skimage.io.imread(x)
    y_data = skimage.io.imread(y)

    image = skopy.feature.Image.measure(x)

    image.intensity = skopy.feature.Intensity.measure(x_data)

    for properties in skimage.measure.regionprops(y_data, x_data):
        instance = skopy.feature.Instance.measure(properties)

        instance.box = skopy.feature.Box.measure(properties)

        instance.intensity = skopy.feature.Intensity.measure(properties.intensity_image)

        instance.shape = skopy.feature.Shape.measure(properties)

        moment_types = [
            (skopy.feature.MomentType.central, properties.moments_central, False),
            (skopy.feature.MomentType.central, properties.weighted_moments_central, True),
            (skopy.feature.MomentType.normalized, properties.moments_normalized, False),
            (skopy.feature.MomentType.normalized, properties.weighted_moments_normalized, True),
            (skopy.feature.MomentType.spatial, properties.moments, False),
            (skopy.feature.MomentType.spatial, properties.weighted_moments, True)
        ]

        for description, moments, weighted in moment_types:
            for p, q in itertools.product(range(0, 3), range(0, 3)):
                moment = skopy.feature.Moment.measure(description, p, q, moments, weighted)

                instance.moments.append(moment)

        moments_zernike = {
            1: mahotas.features.zernike_moments(properties.intensity_image, 1),
            2: mahotas.features.zernike_moments(properties.intensity_image, 2),
            3: mahotas.features.zernike_moments(properties.intensity_image, 3)
        }

        for p, q in itertools.product(range(0, 3), range(0, 25)):
            parameters = {
                "description": skopy.feature.MomentType.zernike,
                "id": uuid.uuid4(),
                "p": p + 1,
                "q": q + 1,
                "weighted": False,
                "y": moments_zernike[p + 1][q],
            }

            moment = skopy.feature.Moment(**parameters)

            instance.moments.append(moment)

        image.instances.append(instance)

    self.session.add(image)

    self.session.commit()
