import numpy
import skimage.exposure
import skimage.filters
import skimage.segmentation
import sklearn.base


def identify_secondary_objects(image, markers, sigma=1):
    """
    Identifies secondary components in an image.
    """
    response = skimage.filters.gaussian(image, sigma)

    mask = response > skimage.filters.threshold_li(response)

    surface = numpy.max(image) - image

    return skimage.segmentation.watershed(surface, markers, mask=mask)


class IdentifySecondaryObjects(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    def __init__(self, sigma=1):
        self.sigma = sigma

    def transform(self, image, markers):
        return identify_secondary_objects(image, markers, self.sigma)
