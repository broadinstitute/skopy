import itertools

import mahotas.features
import numpy
import pandas
import skimage.feature
import skimage.io
import skimage.measure
import skimage.exposure


def combine(dictionaries):
    combined = {}

    for dictionary in dictionaries:
        for key, value in dictionary.items():
            combined.setdefault(key, []).append(value)

    return combined


def extract_local_binary_patterns_features(image, points=None, radius=None):
    if points is None:
        points = [6, 12]

    if radius is None:
        radius = [8, 16]

    def create_keys(name, radius, points):
        triplets = itertools.product(radius, points, range(14))

        return [f"{name}_{key}_{radius}_{points}" for (radius, points, key) in triplets]

    keys = create_keys("local_binary_patterns", radius, points)

    values = []

    for r, p in itertools.product(radius, points):
        features = mahotas.features.lbp(image, r, p)

        values += list(features)

    return dict(zip(keys, values))


def extract_graylevel_cooccurrence_features(image, maximum_distance=8):
    def create_keys(name, key, distances, angles):
        angles = numpy.degrees(angles).astype(numpy.uint16)

        pairs = itertools.product(distances, angles)

        return [f"{name}_{key}_{distance}_{angle:03}" for distance, angle in pairs]

    image = skimage.exposure.rescale_intensity(image, out_range=numpy.uint8)

    image = image.astype(numpy.uint8)

    distances = numpy.arange(1, maximum_distance + 1)

    angles = numpy.arange(4) * numpy.pi / 2  # [0, 90, 180, 270]

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


def extract_threshold_adjacency_statistics_features(image):
    features = {}

    threshold_adjacency_statistics = mahotas.features.tas(image)

    for feature_index, feature in enumerate(threshold_adjacency_statistics):
        features[f"threshold_adjacency_statistics_{feature_index}"] = feature

    return features


def extract_zernike_features(image, degrees=None, radiuses=None):
    if degrees is None:
        degrees = [8]

    if radiuses is None:
        radiuses = [8, 16]

    features = {}

    for degree, radius in itertools.product(degrees, radiuses):
        zernike_moments = mahotas.features.zernike_moments(image, radius, degree)

        for feature_index, feature in enumerate(zernike_moments):
            features[f"moments_zernike_{degree}_{radius}_{feature_index}"] = feature

    return features


def extract_image_features(image):
    extracted_features = {
        "intensity_integrated": numpy.sum(image),
        "intensity_maximum": numpy.max(image),
        "intensity_mean": numpy.mean(image),
        "intensity_median": numpy.median(image),
        "intensity_median_absolute_deviation": numpy.median(numpy.abs(numpy.ma.array(image).compressed() - numpy.median(image))),
        "intensity_minimum": numpy.min(image),
        "intensity_quartile_1": numpy.percentile(image, 25),
        "intensity_quartile_2": numpy.percentile(image, 50),
        "intensity_quartile_3": numpy.percentile(image, 75),
        "intensity_standard_deviation": numpy.std(image)
    }

    texture_features = extract_graylevel_cooccurrence_features(image)

    extracted_features.update(texture_features)

    return pandas.DataFrame.from_dict([extracted_features])


def extract_object_features(image, label_image):
    region_properties = skimage.measure.regionprops(label_image, image)

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
            "intensity_integrated": numpy.sum(region_property.intensity_image),
            "intensity_maximum": region_property.max_intensity,
            "intensity_mean": region_property.mean_intensity,
            "intensity_median": numpy.median(region_property.intensity_image),
            "intensity_median_absolute_deviation": numpy.median(numpy.abs(numpy.ma.array(region_property.intensity_image).compressed() - numpy.median(region_property.intensity_image))),
            "intensity_minimum": region_property.min_intensity,
            "intensity_quartile_1": numpy.percentile(region_property.intensity_image, 25),
            "intensity_quartile_2": numpy.percentile(region_property.intensity_image, 50),
            "intensity_quartile_3": numpy.percentile(region_property.intensity_image, 75),
            "intensity_standard_deviation": numpy.std(region_property.intensity_image),
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
            "moments_weighted_normalized_1_0": region_property.weighted_moments_normalized[1, 0],
            "moments_weighted_normalized_1_1": region_property.weighted_moments_normalized[1, 1],
            "moments_weighted_normalized_1_2": region_property.weighted_moments_normalized[1, 2],
            "moments_weighted_normalized_2_0": region_property.weighted_moments_normalized[2, 0],
            "moments_weighted_normalized_2_1": region_property.weighted_moments_normalized[2, 1],
            "moments_weighted_normalized_2_2": region_property.weighted_moments_normalized[2, 2],
            "moments_weighted_spatial_0_0": region_property.weighted_moments[0, 0],
            "moments_weighted_spatial_0_1": region_property.weighted_moments[0, 1],
            "moments_weighted_spatial_0_2": region_property.weighted_moments[0, 2],
            "moments_weighted_spatial_1_0": region_property.weighted_moments[1, 0],
            "moments_weighted_spatial_1_1": region_property.weighted_moments[1, 1],
            "moments_weighted_spatial_1_2": region_property.weighted_moments[1, 2],
            "moments_weighted_spatial_2_0": region_property.weighted_moments[2, 0],
            "moments_weighted_spatial_2_1": region_property.weighted_moments[2, 1],
            "moments_weighted_spatial_2_2": region_property.weighted_moments[2, 2],
            "orientation": region_property.orientation,
            "perimeter": region_property.perimeter,
            "shannon_entropy_hartley": skimage.measure.shannon_entropy(region_property.intensity_image, base=10),
            "shannon_entropy_natural": skimage.measure.shannon_entropy(region_property.intensity_image, base=numpy.e),
            "shannon_entropy_shannon": skimage.measure.shannon_entropy(region_property.intensity_image, base=2),
            "solidity": region_property.solidity,
        }

        texture_features = extract_graylevel_cooccurrence_features(region_property.intensity_image)

        features.update(texture_features)

        zernike_features = extract_zernike_features(region_property.intensity_image)

        features.update(zernike_features)

        threshold_adjacency_statistics_features = extract_threshold_adjacency_statistics_features(region_property.intensity_image)

        features.update(threshold_adjacency_statistics_features)

        local_binary_patterns_features = extract_local_binary_patterns_features(region_property.intensity_image)

        features.update(local_binary_patterns_features)

        extracted_features.append(features)

    return pandas.DataFrame(combine(extracted_features))
