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
def command(metadata, output):
    if output:
        with contextlib.suppress(FileNotFoundError):
            os.remove(output)

    metadata = pandas.read_csv(metadata)

    metadata = metadata.itertuples()

    progress = click.progressbar(
        [
            (image_pathname, mask_pathname)
            for _, image_pathname, mask_pathname in metadata
        ]
    )

    with progress as metadata:
        for image_pathname, mask_pathname in metadata:
            image = skimage.io.imread(image_pathname)

            mask = skimage.io.imread(mask_pathname)

            features = skopy.feature_extraction.image.extract_object_features(image, mask)

            features["pathname"] = image_pathname
            
            if os.path.exists(output):
                with open(output, "a") as fd:
                    features.to_csv(fd, header=False, index=False)
            else:
                with open(output, "w") as fd:
                    features.to_csv(fd, header=True, index=False)
