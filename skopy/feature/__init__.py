import itertools

import mahotas.features
import skimage.feature
import skimage.io
import skimage.measure

from ._base import Base
from ._box import Box
from ._correlation import Correlation
from ._description import Description
from ._image import Image
from ._instance import Instance
from ._intensity import Intensity
from ._moment import Moment, MomentType
from ._shape import Shape


def describe(image):
    descriptor = skimage.feature.ORB()

    descriptor.detect_and_extract(image)

    descriptions = []

    for index in range(0, len(descriptor.keypoints)):
        description = Description.measure(index, descriptor)

        descriptions.append(description)

    return descriptions


def extract(pathname, mask):
    x_data = skimage.io.imread(pathname)
    y_data = skimage.io.imread(mask)

    image = Image.measure(pathname)

    image.descriptions = describe(x_data)

    image.intensity = Intensity.measure(x_data)

    for properties in skimage.measure.regionprops(y_data, x_data):
        instance = extract_instance(properties)

        image.instances.append(instance)

    return image


def extract_instance(properties):
    instance = Instance.measure(properties)

    instance.box = Box.measure(properties)

    instance.intensity = Intensity.measure(properties.intensity_image)

    instance.shape = Shape.measure(properties)

    moment_types = [
        (MomentType.central, properties.moments_central, False),
        (MomentType.central, properties.weighted_moments_central, True),
        (MomentType.normalized, properties.moments_normalized, False),
        (MomentType.normalized, properties.weighted_moments_normalized, True),
        (MomentType.spatial, properties.moments, False),
        (MomentType.spatial, properties.weighted_moments, True)
    ]

    for description, moments, weighted in moment_types:
        for p, q in itertools.product(range(0, 3), range(0, 3)):
            moment = Moment.measure(description, p, q, moments, weighted)

            instance.moments.append(moment)

    for p, q in itertools.product(range(0, 2), range(0, 2)):
        moment = Moment.measure(MomentType.inertia, p, q, properties.inertia_tensor, False)

        instance.moments.append(moment)

    moments_zernike = {
        1: mahotas.features.zernike_moments(properties.intensity_image, 1),
        2: mahotas.features.zernike_moments(properties.intensity_image, 2),
        3: mahotas.features.zernike_moments(properties.intensity_image, 3)
    }

    for p, q in itertools.product(range(0, 3), range(0, 25)):
        moment = Moment.measure(MomentType.zernike, p, q, moments_zernike, False)

        instance.moments.append(moment)

    return instance
