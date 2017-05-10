# -*- coding: utf-8 -*-

import click
import numpy
import pandas
import psycopg2.extensions
import sqlalchemy
import sqlalchemy.orm

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
    engine = sqlalchemy.create_engine(database, echo=verbose)

    skopy.feature.Base.metadata.drop_all(engine)

    skopy.feature.Base.metadata.create_all(engine)

    session = sqlalchemy.orm.sessionmaker()

    session.configure(bind=engine)

    session = session()

    metadata = pandas.read_csv(metadata)

    images = []

    with click.progressbar([(pathname, mask) for _, pathname, mask in metadata.itertuples()]) as metadata:
        for pathname, mask in metadata:
            image = skopy.feature.extract(pathname, mask)

            images.append(image)

    session.add_all(images)

    session.commit()
