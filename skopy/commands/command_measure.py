# -*- coding: utf-8 -*-

import click
import pandas
import skimage.io
import skimage.measure
import skopy.command
import skopy.features
import sqlalchemy
import sqlalchemy.orm


@click.command("measure")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
@click.option(
    "--connection",
    default="sqlite:///measurements.sqlite",
    nargs=1,
    type=click.STRING
)
@skopy.command.pass_context
def command(context, metadata, connection):
    """

    """
    engine = sqlalchemy.create_engine(connection, echo=True)

    skopy.features.Base.metadata.create_all(engine)

    session = sqlalchemy.orm.sessionmaker()

    session.configure(bind=engine)

    session = session()

    records = pandas.read_csv(metadata)

    image_records = []

    for image_pathname in records["image"].unique():
        image = skimage.io.imread(image_pathname)

        image_record = skopy.features.Image(image_pathname, image)

        image_records.append(image_record)

    session.add_all(image_records)

    instance_records = []

    for _, record in records.iterrows():
        image_pathname = record["image"]
        label_pathname = record["label"]

        image = skimage.io.imread(image_pathname)
        label = skimage.io.imread(label_pathname)

        regions = skimage.measure.regionprops(label, image)

        for region in regions:
            instance_record = skopy.features.Instance(region)

            instance_record.image_pathname = image_pathname
            instance_record.label_pathname = label_pathname

            instance_records.append(instance_record)

    session.add_all(instance_records)

    session.commit()
