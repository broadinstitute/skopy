# -*- coding: utf-8 -*-

import click
import itertools
import pandas
import skopy.command
import skopy.features
import sqlalchemy
import sqlalchemy.orm


@click.command("measure")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
@click.option("--database", default="sqlite:///measurements.sqlite")
@click.option("--verbose", is_flag=True)
@skopy.command.pass_context
def command(context, metadata, database, verbose):
    """

    """
    engine = sqlalchemy.create_engine(database, echo=verbose)

    skopy.features.Base.metadata.create_all(engine)

    session = sqlalchemy.orm.sessionmaker()

    session.configure(bind=engine)

    session = session()

    records = pandas.read_csv(metadata)

    for _, record in records.iterrows():
        image = skopy.features.Image(record["image"], record["label"])

        session.add(image)

    for x, y in itertools.product(records["image"].unique(), records["label"].unique()):
        correlation = skopy.features.Correlation(x, y)

        session.add(correlation)

    session.commit()
