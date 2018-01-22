import mahotas
import numpy
import skimage.exposure
import skimage.filters
import skimage.segmentation
import sklearn.base


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


class IdentifyPrimaryObjects(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    def __init__(self, footprint=(16, 16), sigma=1):
        self.footprint = footprint

        self.sigma = sigma

    def transform(self, image):
        return identify_primary_objects(image, self.footprint, self.sigma)
