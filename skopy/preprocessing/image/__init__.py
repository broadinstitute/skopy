import mahotas
import numpy
import skimage.exposure
import skimage.filters
import skimage.segmentation


def label(x, y):
    x, _, _ = skimage.segmentation.relabel_sequential(x)
    y, _, _ = skimage.segmentation.relabel_sequential(y)

    x = skimage.img_as_uint(x, force_copy=True)
    y = skimage.img_as_uint(y, force_copy=True)

    x_n = len(numpy.unique(x))
    y_n = len(numpy.unique(y))

    union, _ = numpy.histogram(y, y_n)

    union = numpy.expand_dims(union, 0)

    flattened_x = x.flatten()
    flattened_y = y.flatten()

    intersection, _, _ = numpy.histogram2d(
        flattened_x,
        flattened_y,
        (x_n, y_n)
    )

    scores = intersection / union

    objects = numpy.argmax(scores, 0)

    modified = numpy.where(objects != numpy.arange(objects.shape[0]))

    if modified[0].shape[0] > 0:
        updated = numpy.zeros_like(y)

        for index in range(objects.shape[0]):
            updated[y == index] = objects[index]

        y = updated

    return x, y


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
