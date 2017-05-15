import os.path

import click
import pandas
import sqlalchemy
import sqlalchemy.orm

import skopy.command
import skopy.feature
import skopy.task


@click.command("measure")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
@click.option("--database", default="sqlite:///measurements.sqlite")
@click.option("--distribute", is_flag=True)
@click.option("--verbose", is_flag=True)
def command(metadata, database, distribute, verbose):
    if distribute:
        pass
    else:
        engine = sqlalchemy.create_engine(database, echo=verbose)

        skopy.feature.Base.metadata.drop_all(engine)

        skopy.feature.Base.metadata.create_all(engine)

        session = sqlalchemy.orm.sessionmaker()

        session.configure(bind=engine)

        session = session()

    directory = os.path.dirname(metadata)

    directory = os.path.abspath(directory)

    metadata = pandas.read_csv(metadata)

    progress = click.progressbar([(pathname, mask) for _, pathname, mask in metadata.itertuples()])

    with progress as metadata:
        for pathname, mask in metadata:
            pathname = os.path.join(directory, pathname)

            mask = os.path.join(directory, mask)

            if distribute:
                skopy.task.measure.delay(database, pathname, mask)
            else:
                image = skopy.feature.extract(pathname, mask)

                session.add(image)

                session.commit()
