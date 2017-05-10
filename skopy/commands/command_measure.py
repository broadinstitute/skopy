# -*- coding: utf-8 -*-

import itertools
import uuid

import click
import mahotas.features
import pandas
import skimage.io
import skimage.measure
import sqlalchemy
import sqlalchemy.orm
import numpy
import psycopg2.extensions

import skopy.command
import skopy.feature

psycopg2.extensions.register_adapter(numpy.float64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.uint64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.uint8, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.int64, psycopg2.extensions.AsIs)

@click.command("measure")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
@click.option("--database", default="sqlite:///measurements.sqlite")
@click.option("--verbose", is_flag=True)
def command(metadata, database, verbose):
    """

    """

    engine = sqlalchemy.create_engine(database, echo=verbose)

    skopy.feature.Base.metadata.drop_all(engine)

    skopy.feature.Base.metadata.create_all(engine)

    session = sqlalchemy.orm.sessionmaker()

    session.configure(bind=engine)

    session = session()

    metadata = pandas.read_csv(metadata)

    pairs = [(image, mask) for _, image, mask in metadata.itertuples()]

    images = []

    with click.progressbar(pairs) as pairs:
        for pathname, mask in pairs:
            x_data = skimage.io.imread(pathname)
            y_data = skimage.io.imread(mask)

            image = skopy.feature.Image.measure(pathname)

            image.intensity = skopy.feature.Intensity.measure(x_data)

            images.append(image)

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

                for p, q in itertools.product(range(0, 2), range(0, 2)):
                    moment = skopy.feature.Moment.measure(skopy.feature.MomentType.inertia, p, q, properties.inertia_tensor, False)

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

    session.add_all(images)

    session.commit()
