import itertools

import mahotas.features
import skimage.feature
import skimage.io
import skimage.measure

from _box import Box
from _description import Description
from _image import Image
from _instance import Instance
from _intensity import Intensity
from _moment import Moment, MomentType
from _shape import Shape


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


def extract_texture_features(crop, maximum_distance=8):
    def create_keys(name, key, distances, angles):
        angles = numpy.degrees(angles).astype(numpy.uint16)

        pairs = itertools.product(distances, angles)

        return [f"{name}_{key}_{distance}_{angle:03}" for distance, angle in
                pairs]

    crop = skimage.exposure.rescale_intensity(crop, out_range=numpy.uint8)

    crop = crop.astype(numpy.uint8)

    distances = numpy.arange(1, maximum_distance + 1)

    angles = numpy.arange(4) * numpy.pi / 2  # [0, 90, 180, 270]

    graylevel_cooccurrence_matrix = skimage.feature.greycomatrix(crop,
                                                                 distances,
                                                                 angles,
                                                                 symmetric=True,
                                                                 normed=True)

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
        values = skimage.feature.greycoprops(graylevel_cooccurrence_matrix,
                                             key)

        values = values.ravel()

        if key == "ASM":
            key = "angular_second_moment"

        keys = create_keys("graylevel_cooccurrence_matrix", key, distances,
                           angles)

        texture_features.update(dict(zip(keys, values)))

    return texture_features


def combine(dictionaries):
    combined = {}

    for dictionary in dictionaries:
        for key, value in dictionary.items():
            combined.setdefault(key, []).append(value)

    return combined


def extract_features(image, labels):
    region_properties = skimage.measure.regionprops(labels, image)

    extracted_features = []

    for region_property in region_properties:
        features = {
            "area": region_property.area,
            "bounding_box_area": region_property.bbox_area,
            "bounding_box_maximum_column": region_property.bbox[3],
            "bounding_box_maximum_row": region_property.bbox[2],
            "bounding_box_minimum_column": region_property.bbox[1],
            "bounding_box_minimum_row": region_property.bbox[0],
            "centroid_column": region_property.centroid[1],
            "centroid_row": region_property.centroid[0],
            "centroid_weighted_column": region_property.weighted_centroid[1],
            "centroid_weighted_local_column": region_property.weighted_local_centroid[1],
            "centroid_weighted_local_row": region_property.weighted_local_centroid[0],
            "centroid_weighted_row": region_property.weighted_centroid[0],
            "convex_hull_area": region_property.convex_area,
            "eccentricity": region_property.eccentricity,
            "equivalent_diameter": region_property.equivalent_diameter,
            "euler_number": region_property.euler_number,
            "extent": region_property.extent,
            "inertia_tensor_0_0": region_property.inertia_tensor[0, 0],
            "inertia_tensor_0_1": region_property.inertia_tensor[0, 1],
            "inertia_tensor_1_0": region_property.inertia_tensor[1, 0],
            "inertia_tensor_1_1": region_property.inertia_tensor[1, 1],
            "inertia_tensor_eigen_values_0": region_property.inertia_tensor_eigvals[0],
            "inertia_tensor_eigen_values_1": region_property.inertia_tensor_eigvals[1],
            "intensity_maximum": region_property.max_intensity,
            "intensity_mean": region_property.mean_intensity,
            "intensity_minimum": region_property.min_intensity,
            "label": region_property.label,
            "major_axis_length": region_property.major_axis_length,
            "minor_axis_length": region_property.minor_axis_length,
            "moments_central_0_0": region_property.moments_central[0, 0],
            "moments_central_0_1": region_property.moments_central[0, 1],
            "moments_central_0_2": region_property.moments_central[0, 2],
            "moments_central_1_0": region_property.moments_central[1, 0],
            "moments_central_1_1": region_property.moments_central[1, 1],
            "moments_central_1_2": region_property.moments_central[1, 2],
            "moments_central_2_0": region_property.moments_central[2, 0],
            "moments_central_2_1": region_property.moments_central[2, 1],
            "moments_central_2_2": region_property.moments_central[2, 2],
            "moments_hu_0": region_property.moments_hu[0],
            "moments_hu_1": region_property.moments_hu[1],
            "moments_hu_2": region_property.moments_hu[2],
            "moments_hu_3": region_property.moments_hu[3],
            "moments_hu_4": region_property.moments_hu[4],
            "moments_hu_5": region_property.moments_hu[5],
            "moments_hu_6": region_property.moments_hu[6],
            "moments_hu_weighted_0": region_property.weighted_moments_hu[0],
            "moments_hu_weighted_1": region_property.weighted_moments_hu[1],
            "moments_hu_weighted_2": region_property.weighted_moments_hu[2],
            "moments_hu_weighted_3": region_property.weighted_moments_hu[3],
            "moments_hu_weighted_4": region_property.weighted_moments_hu[4],
            "moments_hu_weighted_5": region_property.weighted_moments_hu[5],
            "moments_hu_weighted_6": region_property.weighted_moments_hu[6],
            "moments_normalized_0_0": region_property.moments_normalized[0, 0],
            "moments_normalized_0_1": region_property.moments_normalized[0, 1],
            "moments_normalized_0_2": region_property.moments_normalized[0, 2],
            "moments_normalized_1_0": region_property.moments_normalized[1, 0],
            "moments_normalized_1_1": region_property.moments_normalized[1, 1],
            "moments_normalized_1_2": region_property.moments_normalized[1, 2],
            "moments_normalized_2_0": region_property.moments_normalized[2, 0],
            "moments_normalized_2_1": region_property.moments_normalized[2, 1],
            "moments_normalized_2_2": region_property.moments_normalized[2, 2],
            "moments_spatial_0_0": region_property.moments[0, 0],
            "moments_spatial_0_1": region_property.moments[0, 1],
            "moments_spatial_0_2": region_property.moments[0, 2],
            "moments_spatial_1_0": region_property.moments[1, 0],
            "moments_spatial_1_1": region_property.moments[1, 1],
            "moments_spatial_1_2": region_property.moments[1, 2],
            "moments_spatial_2_0": region_property.moments[2, 0],
            "moments_spatial_2_1": region_property.moments[2, 1],
            "moments_spatial_2_2": region_property.moments[2, 2],
            "moments_weighted_central_0_0": region_property.weighted_moments_central[0, 0],
            "moments_weighted_central_0_1": region_property.weighted_moments_central[0, 1],
            "moments_weighted_central_0_2": region_property.weighted_moments_central[0, 2],
            "moments_weighted_central_1_0": region_property.weighted_moments_central[1, 0],
            "moments_weighted_central_1_1": region_property.weighted_moments_central[1, 1],
            "moments_weighted_central_1_2": region_property.weighted_moments_central[1, 2],
            "moments_weighted_central_2_0": region_property.weighted_moments_central[2, 0],
            "moments_weighted_central_2_1": region_property.weighted_moments_central[2, 1],
            "moments_weighted_central_2_2": region_property.weighted_moments_central[2, 2],
            "moments_weighted_normalized_0_0": region_property.weighted_moments_normalized[0, 0],
            "moments_weighted_normalized_0_1": region_property.weighted_moments_normalized[0, 1],
            "moments_weighted_normalized_0_2": region_property.weighted_moments_normalized[0, 2],
            "moments_weighted_normalized_1_0":
                region_property.weighted_moments_normalized[1, 0],
            "moments_weighted_normalized_1_1":
                region_property.weighted_moments_normalized[1, 1],
            "moments_weighted_normalized_1_2":
                region_property.weighted_moments_normalized[1, 2],
            "moments_weighted_normalized_2_0":
                region_property.weighted_moments_normalized[2, 0],
            "moments_weighted_normalized_2_1":
                region_property.weighted_moments_normalized[2, 1],
            "moments_weighted_normalized_2_2":
                region_property.weighted_moments_normalized[2, 2],
            "moments_weighted_spatial_0_0": region_property.weighted_moments[
                0, 0],
            "moments_weighted_spatial_0_1": region_property.weighted_moments[
                0, 1],
            "moments_weighted_spatial_0_2": region_property.weighted_moments[
                0, 2],
            "moments_weighted_spatial_1_0": region_property.weighted_moments[
                1, 0],
            "moments_weighted_spatial_1_1": region_property.weighted_moments[
                1, 1],
            "moments_weighted_spatial_1_2": region_property.weighted_moments[
                1, 2],
            "moments_weighted_spatial_2_0": region_property.weighted_moments[
                2, 0],
            "moments_weighted_spatial_2_1": region_property.weighted_moments[
                2, 1],
            "moments_weighted_spatial_2_2": region_property.weighted_moments[
                2, 2],
            "orientation": region_property.orientation,
            "perimeter": region_property.perimeter,
            "shannon_entropy_hartley": skimage.measure.shannon_entropy(
                region_property.intensity_image, base=10),
            "shannon_entropy_natural": skimage.measure.shannon_entropy(
                region_property.intensity_image, base=numpy.e),
            "shannon_entropy_shannon": skimage.measure.shannon_entropy(
                region_property.intensity_image, base=2),
            "solidity": region_property.solidity,
        }

        texture_features = extract_texture_features(
            region_property.intensity_image)

        features.update(texture_features)

        extracted_features.append(features)

    return pandas.DataFrame(combine(extracted_features))
