import mahotas
import numpy
import skimage.exposure
import skimage.filters
import skimage.segmentation


def identify_primary_objects(image, footprint=(16, 16), sigma=1):
    """
    Identifies primary components in an image.
    """
    response = skimage.filters.gaussian(image, sigma)

    mask = response > skimage.filters.threshold_li(response)

    image = mahotas.distance(mask)

    image = skimage.exposure.rescale_intensity(image)

    footprint = numpy.ones(footprint)

    markers = mahotas.regmax(image, footprint)

    markers, _ = mahotas.label(markers, footprint)

    image = numpy.max(image) - image

    return skimage.segmentation.watershed(image, markers, mask=mask)


def identify_secondary_objects(image, markers, sigma=1):
    """
    Identifies secondary components in an image.
    """
    response = skimage.filters.gaussian(image, sigma)

    mask = response > skimage.filters.threshold_li(response)

    surface = numpy.max(image) - image

    return skimage.segmentation.watershed(surface, markers, mask=mask)
