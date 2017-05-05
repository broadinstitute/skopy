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

    image_records = []

    with click.progressbar(records["image"].unique(), label="measuring images", length=len(records["image"].unique())) as image_pathnames:
        for image_pathname in image_pathnames:
            image = skimage.io.imread(image_pathname)

            image_record = skopy.features.Image(image_pathname, image)

            image_records.append(image_record)

    session.add_all(image_records)

    instance_records = []

    with click.progressbar(records.iterrows(), label="measuring objects", length=len(records)) as records:
        for _, record in records:
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
