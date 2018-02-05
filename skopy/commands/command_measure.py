import contextlib
import os.path

import click
import pandas

import skimage.io

import skopy.command
import skopy.feature_extraction.image


@click.command("measure")
@click.argument("metadata", nargs=1, type=click.Path(exists=True))
@click.option("--output", "-o", nargs=1, type=click.Path())
def command(metadata, output_pathname):
    if output_pathname:
        with contextlib.suppress(FileNotFoundError):
            os.remove(output_pathname)

    metadata = pandas.read_csv(metadata)

    metadata = metadata.itertuples()

    progress = click.progressbar(
        [
            (image_pathname, mask_pathname, description)
            for _, image_pathname, mask_pathname, description in metadata
        ]
    )

    with progress as metadata:
        for image_pathname, mask_pathname, description in metadata:
            image = skimage.io.imread(image_pathname)

            mask = skimage.io.imread(mask_pathname)

            features = skopy.feature_extraction.image.extract_object_features(image, mask)

            if os.path.exists(output_pathname):
                with open(output_pathname, "a") as fd:
                    features.to_csv(fd, header=False, index=False)
            else:
                with open(output_pathname, "w") as fd:
                    features.to_csv(fd, header=True, index=False)
