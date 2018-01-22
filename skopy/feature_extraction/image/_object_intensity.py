import numpy
import skimage.measure


feature_names = [
    "integrated",
    "maximum",
    "mean",
    "median",
    "median_absolute_deviation",
    "minimum",
    "quartile_1",
    "quartile_2",
    "quartile_3",
    "standard_deviation"
]


def extract_object_intensity_features(image, mask):
    properties = skimage.measure.regionprops(mask, image)

    intensity_features = numpy.zeros((len(properties), len(feature_names)))

    for index, properties in enumerate(properties):
        features = [
            numpy.sum(properties.intensity_image),
            numpy.max(properties.intensity_image),
            numpy.mean(properties.intensity_image),
            numpy.median(properties.intensity_image),
            numpy.median(numpy.abs(numpy.ma.array(properties.intensity_image).compressed() - numpy.median(properties.intensity_image))),
            numpy.min(properties.intensity_image),
            numpy.percentile(properties.intensity_image, 25),
            numpy.percentile(properties.intensity_image, 50),
            numpy.percentile(properties.intensity_image, 75),
            numpy.std(properties.intensity_image)
        ]

        intensity_features[index] = features

    return intensity_features
