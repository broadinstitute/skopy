import itertools

import numpy
import skimage.exposure
import skimage.feature


def extract_texture_features(image, maximum_distance=8):
    def create_keys(name, key, distances, angles):
        angles = numpy.degrees(angles).astype(numpy.uint16)

        pairs = itertools.product(distances, angles)

        return [f"{name}_{key}_{distance}_{angle:03}" for distance, angle in pairs]

    image = skimage.exposure.rescale_intensity(image, out_range=numpy.uint8)

    image = skimage.img_as_ubyte(image)

    distances = numpy.arange(1, maximum_distance + 1)

    angles = numpy.arange(4) * numpy.pi / 2

    graylevel_cooccurrence_matrix = skimage.feature.greycomatrix(image, distances, angles, symmetric=True, normed=True)

    keys = [
        "ASM",
        "contrast",
        "correlation",
        "dissimilarity",
        "energy",
        "homogeneity"
    ]

    texture_features = {}

    for key in keys:
        values = skimage.feature.greycoprops(graylevel_cooccurrence_matrix, key)

        values = values.ravel()

        if key == "ASM":
            key = "angular_second_moment"

        keys = create_keys("graylevel_cooccurrence_matrix", key, distances, angles)

        texture_features.update(dict(zip(keys, values)))

    return texture_features
