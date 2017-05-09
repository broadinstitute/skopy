# -*- coding: utf-8 -*-

import itertools

import click
import pandas
import sqlalchemy
import sqlalchemy.orm

import skopy.command
import skopy.feature


@click.command("measure")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
@click.option("--database", default="sqlite:///measurements.sqlite")
@click.option("--verbose", is_flag=False)
def command(metadata, database, verbose):
    """

    """
    engine = sqlalchemy.create_engine(database, echo=verbose)

    skopy.feature.Base.metadata.create_all(engine)

    session = sqlalchemy.orm.sessionmaker()

    session.configure(bind=engine)

    session = session()

    metadata = pandas.read_csv(metadata)

    pairs = [(image, mask) for _, image, mask in metadata.itertuples()]

    with click.progressbar(pairs) as pairs:
        for pathname, mask in pairs:
            image = skopy.feature.Image(pathname, mask)

            session.add(image)

    pairs = itertools.product(metadata["image"].unique(), metadata["label"].unique())

    for x, y in pairs:
        correlation = skopy.feature.Correlation(x, y)

        session.add(correlation)

    session.commit()
