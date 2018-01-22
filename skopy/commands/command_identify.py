import os.path

import click
import numpy
import scipy.ndimage
import skimage.exposure
import skimage.feature
import skimage.filters
import skimage.io
import skimage.measure
import skimage.segmentation

import skopy.command


@click.command("identify")
@click.argument(
    "images",
    nargs=-1,
    type=click.Path(exists=True)
)
@click.option(
    "--sigma",
    default=1,
    help="Standard deviation for Gaussian kernel. The standard deviations of "
         "the Gaussian filter are given for each axis as a sequence, or as a "
         "single number, in which case it is equal for all axes.             "
)
@click.option(
    "--footprint",
    default=16,
    help="The footprint represents the local region within which to search   "
         "for peaks at every point in an image.                              "
)
@click.option(
    "--output",
    default="."
)
def command(images, sigma, footprint, output):
    progress = click.progressbar([image for image in images])

    with progress as images:
        for image in images:
            data = skimage.io.imread(image)

            response = skimage.filters.gaussian(data, sigma)

            threshold = skimage.filters.threshold_isodata(response)

            mask = numpy.zeros_like(response, numpy.uint8)

            mask[response > threshold] = 255

            mask = skimage.exposure.rescale_intensity(mask)

            distance = scipy.ndimage.distance_transform_edt(mask)

            distance = skimage.exposure.rescale_intensity(distance)

            footprint = numpy.ones((footprint, footprint))

            peaks = skimage.feature.peak_local_max(
                distance,
                indices=False,
                footprint=footprint
            )

            markers = skimage.measure.label(peaks)

            labels = skimage.segmentation.watershed(-distance, markers)

            labels *= mask

            pathname = os.path.join(output, os.path.basename(image))

            skimage.io.imsave(pathname, labels)
