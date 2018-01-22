import numpy
import skimage.measure


feature_names = [
    "area",
    "axis_major",
    "axis_minor",
    "convex_area",
    "eccentricity",
    "equivalent_diameter",
    "euler_number",
    "extent",
    "orientation",
    "perimeter",
    "solidity"
]


def extract_shape_features(image, mask):
    properties = skimage.measure.regionprops(mask, image)

    shape_features = numpy.zeros((len(properties), len(feature_names)))

    for index, properties in enumerate(properties):
        features = [
            properties.area,
            properties.major_axis_length,
            properties.minor_axis_length,
            properties.convex_area,
            properties.eccentricity,
            properties.equivalent_diameter,
            properties.euler_number,
            properties.extent,
            properties.orientation,
            properties.perimeter,
            properties.solidity
        ]

        shape_features[index] = features

    return shape_features
