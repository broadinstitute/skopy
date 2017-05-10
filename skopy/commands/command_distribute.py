import os.path

import click
import pandas

from skopy.task import measure


@click.command("distribute")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
def command(metadata):
    """

    """
    for _, pair in pandas.read_csv(metadata).iterrows():
        directory = os.path.dirname(metadata)

        directory = os.path.abspath(directory)

        x = os.path.join(directory, pair["image"])
        y = os.path.join(directory, pair["label"])

        measure.delay(x, y)
