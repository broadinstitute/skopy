import mahotas.features
import skimage.measure
import sqlalchemy
import sqlalchemy.orm

from ._base import Base
from ._box import Box
from ._intensity import Intensity
from ._moment import Moment, MomentType


class Instance(Base):
    __tablename__ = "instances"

    axis_major = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    axis_minor = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    box = sqlalchemy.orm.relationship("Box", backref=sqlalchemy.orm.backref("instance", uselist=False))
    box_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("boxes.id"), nullable=False, unique=True)

    centroid_weighted_local_x = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    centroid_weighted_local_y = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    centroid_weighted_x = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    centroid_weighted_y = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    centroid_x = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    centroid_y = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    eccentricity = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    equivalent_diameter = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    euler_number = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    extent = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("images.id"), nullable=False)

    index = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    inertia_tensor_1_1 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    inertia_tensor_1_2 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    inertia_tensor_2_1 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    inertia_tensor_2_2 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    inertia_tensor_eigvals_1 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    inertia_tensor_eigvals_2 = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    intensity = sqlalchemy.orm.relationship("Intensity", backref=sqlalchemy.orm.backref("instance", uselist=False))
    intensity_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("intensities.id"), nullable=False, unique=True)

    moments = sqlalchemy.orm.relationship("Moment", backref="instance")

    orientation = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    pathname = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    perimeter = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    shannon_entropy = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    solidity = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    def __init__(self, pathname, properties):
        self.pathname = pathname

        self.area = properties.area

        self.axis_major = properties.major_axis_length
        self.axis_minor = properties.minor_axis_length

        self.box = Box(properties)

        self.centroid_weighted_local_x = properties.weighted_local_centroid[0]
        self.centroid_weighted_local_y = properties.weighted_local_centroid[1]

        self.centroid_weighted_x = properties.weighted_centroid[0]
        self.centroid_weighted_y = properties.weighted_centroid[1]

        self.centroid_x = properties.centroid[0]
        self.centroid_y = properties.centroid[1]

        self.convex_area = properties.convex_area

        self.eccentricity = properties.eccentricity

        self.equivalent_diameter = properties.equivalent_diameter

        self.euler_number = properties.euler_number

        self.extent = properties.extent

        self.filled_area = properties.filled_area

        self.index = properties.label

        self.inertia_tensor_1_1 = properties.inertia_tensor[0, 0]
        self.inertia_tensor_1_2 = properties.inertia_tensor[0, 1]
        self.inertia_tensor_2_1 = properties.inertia_tensor[1, 0]
        self.inertia_tensor_2_2 = properties.inertia_tensor[1, 1]

        self.inertia_tensor_eigvals_1 = properties.inertia_tensor_eigvals[0]
        self.inertia_tensor_eigvals_2 = properties.inertia_tensor_eigvals[1]

        self.intensity = Intensity(properties.intensity_image)

        moments_zernike_01 = mahotas.features.zernike_moments(properties.intensity_image, 1)
        moments_zernike_02 = mahotas.features.zernike_moments(properties.intensity_image, 2)
        moments_zernike_03 = mahotas.features.zernike_moments(properties.intensity_image, 3)

        moments = [
            Moment(MomentType.central, 1, 1, properties.moments_central[0, 0]),
            Moment(MomentType.central, 1, 2, properties.moments_central[0, 1]),
            Moment(MomentType.central, 1, 3, properties.moments_central[0, 2]),
            Moment(MomentType.central, 2, 1, properties.moments_central[1, 0]),
            Moment(MomentType.central, 2, 2, properties.moments_central[1, 1]),
            Moment(MomentType.central, 2, 3, properties.moments_central[1, 2]),
            Moment(MomentType.central, 3, 1, properties.moments_central[2, 0]),
            Moment(MomentType.central, 3, 2, properties.moments_central[2, 1]),
            Moment(MomentType.central, 3, 3, properties.moments_central[2, 2]),

            Moment(MomentType.central, 1, 1, properties.weighted_moments_central[0, 0], weighted=True),
            Moment(MomentType.central, 1, 2, properties.weighted_moments_central[0, 1], weighted=True),
            Moment(MomentType.central, 1, 3, properties.weighted_moments_central[0, 2], weighted=True),
            Moment(MomentType.central, 2, 1, properties.weighted_moments_central[1, 0], weighted=True),
            Moment(MomentType.central, 2, 2, properties.weighted_moments_central[1, 1], weighted=True),
            Moment(MomentType.central, 2, 3, properties.weighted_moments_central[1, 2], weighted=True),
            Moment(MomentType.central, 3, 1, properties.weighted_moments_central[2, 0], weighted=True),
            Moment(MomentType.central, 3, 2, properties.weighted_moments_central[2, 1], weighted=True),
            Moment(MomentType.central, 3, 3, properties.weighted_moments_central[2, 2], weighted=True),

            Moment(MomentType.normalized, 1, 1, properties.moments_normalized[0, 0]),
            Moment(MomentType.normalized, 1, 2, properties.moments_normalized[0, 1]),
            Moment(MomentType.normalized, 1, 3, properties.moments_normalized[0, 2]),
            Moment(MomentType.normalized, 2, 1, properties.moments_normalized[1, 0]),
            Moment(MomentType.normalized, 2, 2, properties.moments_normalized[1, 1]),
            Moment(MomentType.normalized, 2, 3, properties.moments_normalized[1, 2]),
            Moment(MomentType.normalized, 3, 1, properties.moments_normalized[2, 0]),
            Moment(MomentType.normalized, 3, 2, properties.moments_normalized[2, 1]),
            Moment(MomentType.normalized, 3, 3, properties.moments_normalized[2, 2]),

            Moment(MomentType.normalized, 1, 1, properties.weighted_moments_normalized[0, 0], weighted=True),
            Moment(MomentType.normalized, 1, 2, properties.weighted_moments_normalized[0, 1], weighted=True),
            Moment(MomentType.normalized, 1, 3, properties.weighted_moments_normalized[0, 2], weighted=True),
            Moment(MomentType.normalized, 2, 1, properties.weighted_moments_normalized[1, 0], weighted=True),
            Moment(MomentType.normalized, 2, 2, properties.weighted_moments_normalized[1, 1], weighted=True),
            Moment(MomentType.normalized, 2, 3, properties.weighted_moments_normalized[1, 2], weighted=True),
            Moment(MomentType.normalized, 3, 1, properties.weighted_moments_normalized[2, 0], weighted=True),
            Moment(MomentType.normalized, 3, 2, properties.weighted_moments_normalized[2, 1], weighted=True),
            Moment(MomentType.normalized, 3, 3, properties.weighted_moments_normalized[2, 2], weighted=True),

            Moment(MomentType.spatial, 1, 1, properties.moments[0, 0]),
            Moment(MomentType.spatial, 1, 2, properties.moments[0, 1]),
            Moment(MomentType.spatial, 1, 3, properties.moments[0, 2]),
            Moment(MomentType.spatial, 2, 1, properties.moments[1, 0]),
            Moment(MomentType.spatial, 2, 2, properties.moments[1, 1]),
            Moment(MomentType.spatial, 2, 3, properties.moments[1, 2]),
            Moment(MomentType.spatial, 3, 1, properties.moments[2, 0]),
            Moment(MomentType.spatial, 3, 2, properties.moments[2, 1]),
            Moment(MomentType.spatial, 3, 3, properties.moments[2, 2]),

            Moment(MomentType.normalized, 1, 1, properties.weighted_moments[0, 0], weighted=True),
            Moment(MomentType.normalized, 1, 2, properties.weighted_moments[0, 1], weighted=True),
            Moment(MomentType.normalized, 1, 3, properties.weighted_moments[0, 2], weighted=True),
            Moment(MomentType.normalized, 2, 1, properties.weighted_moments[1, 0], weighted=True),
            Moment(MomentType.normalized, 2, 2, properties.weighted_moments[1, 1], weighted=True),
            Moment(MomentType.normalized, 2, 3, properties.weighted_moments[1, 2], weighted=True),
            Moment(MomentType.normalized, 3, 1, properties.weighted_moments[2, 0], weighted=True),
            Moment(MomentType.normalized, 3, 2, properties.weighted_moments[2, 1], weighted=True),
            Moment(MomentType.normalized, 3, 3, properties.weighted_moments[2, 2], weighted=True),

            Moment(MomentType.zernike, 1, 1, moments_zernike_01[0]),
            Moment(MomentType.zernike, 1, 2, moments_zernike_01[1]),
            Moment(MomentType.zernike, 1, 3, moments_zernike_01[2]),
            Moment(MomentType.zernike, 1, 4, moments_zernike_01[3]),
            Moment(MomentType.zernike, 1, 5, moments_zernike_01[4]),
            Moment(MomentType.zernike, 1, 6, moments_zernike_01[5]),
            Moment(MomentType.zernike, 1, 7, moments_zernike_01[6]),
            Moment(MomentType.zernike, 1, 8, moments_zernike_01[7]),
            Moment(MomentType.zernike, 1, 9, moments_zernike_01[8]),
            Moment(MomentType.zernike, 1, 10, moments_zernike_01[9]),
            Moment(MomentType.zernike, 1, 11, moments_zernike_01[10]),
            Moment(MomentType.zernike, 1, 12, moments_zernike_01[11]),
            Moment(MomentType.zernike, 1, 13, moments_zernike_01[12]),
            Moment(MomentType.zernike, 1, 14, moments_zernike_01[13]),
            Moment(MomentType.zernike, 1, 15, moments_zernike_01[14]),
            Moment(MomentType.zernike, 1, 16, moments_zernike_01[15]),
            Moment(MomentType.zernike, 1, 17, moments_zernike_01[16]),
            Moment(MomentType.zernike, 1, 18, moments_zernike_01[17]),
            Moment(MomentType.zernike, 1, 19, moments_zernike_01[18]),
            Moment(MomentType.zernike, 1, 20, moments_zernike_01[19]),
            Moment(MomentType.zernike, 1, 21, moments_zernike_01[20]),
            Moment(MomentType.zernike, 1, 22, moments_zernike_01[21]),
            Moment(MomentType.zernike, 1, 23, moments_zernike_01[22]),
            Moment(MomentType.zernike, 1, 24, moments_zernike_01[23]),
            Moment(MomentType.zernike, 1, 25, moments_zernike_01[24]),
            Moment(MomentType.zernike, 2, 1, moments_zernike_02[0]),
            Moment(MomentType.zernike, 2, 2, moments_zernike_02[1]),
            Moment(MomentType.zernike, 2, 3, moments_zernike_02[2]),
            Moment(MomentType.zernike, 2, 4, moments_zernike_02[3]),
            Moment(MomentType.zernike, 2, 5, moments_zernike_02[4]),
            Moment(MomentType.zernike, 2, 6, moments_zernike_02[5]),
            Moment(MomentType.zernike, 2, 7, moments_zernike_02[6]),
            Moment(MomentType.zernike, 2, 8, moments_zernike_02[7]),
            Moment(MomentType.zernike, 2, 9, moments_zernike_02[8]),
            Moment(MomentType.zernike, 2, 10, moments_zernike_02[9]),
            Moment(MomentType.zernike, 2, 11, moments_zernike_02[10]),
            Moment(MomentType.zernike, 2, 12, moments_zernike_02[11]),
            Moment(MomentType.zernike, 2, 13, moments_zernike_02[12]),
            Moment(MomentType.zernike, 2, 14, moments_zernike_02[13]),
            Moment(MomentType.zernike, 2, 15, moments_zernike_02[14]),
            Moment(MomentType.zernike, 2, 16, moments_zernike_02[15]),
            Moment(MomentType.zernike, 2, 17, moments_zernike_02[16]),
            Moment(MomentType.zernike, 2, 18, moments_zernike_02[17]),
            Moment(MomentType.zernike, 2, 19, moments_zernike_02[18]),
            Moment(MomentType.zernike, 2, 20, moments_zernike_02[19]),
            Moment(MomentType.zernike, 2, 21, moments_zernike_02[20]),
            Moment(MomentType.zernike, 2, 22, moments_zernike_02[21]),
            Moment(MomentType.zernike, 2, 23, moments_zernike_02[22]),
            Moment(MomentType.zernike, 2, 24, moments_zernike_02[23]),
            Moment(MomentType.zernike, 2, 25, moments_zernike_02[24]),
            Moment(MomentType.zernike, 3, 1, moments_zernike_03[0]),
            Moment(MomentType.zernike, 3, 2, moments_zernike_03[1]),
            Moment(MomentType.zernike, 3, 3, moments_zernike_03[2]),
            Moment(MomentType.zernike, 3, 4, moments_zernike_03[3]),
            Moment(MomentType.zernike, 3, 5, moments_zernike_03[4]),
            Moment(MomentType.zernike, 3, 6, moments_zernike_03[5]),
            Moment(MomentType.zernike, 3, 7, moments_zernike_03[6]),
            Moment(MomentType.zernike, 3, 8, moments_zernike_03[7]),
            Moment(MomentType.zernike, 3, 9, moments_zernike_03[8]),
            Moment(MomentType.zernike, 3, 10, moments_zernike_03[9]),
            Moment(MomentType.zernike, 3, 11, moments_zernike_03[10]),
            Moment(MomentType.zernike, 3, 12, moments_zernike_03[11]),
            Moment(MomentType.zernike, 3, 13, moments_zernike_03[12]),
            Moment(MomentType.zernike, 3, 14, moments_zernike_03[13]),
            Moment(MomentType.zernike, 3, 15, moments_zernike_03[14]),
            Moment(MomentType.zernike, 3, 16, moments_zernike_03[15]),
            Moment(MomentType.zernike, 3, 17, moments_zernike_03[16]),
            Moment(MomentType.zernike, 3, 18, moments_zernike_03[17]),
            Moment(MomentType.zernike, 3, 19, moments_zernike_03[18]),
            Moment(MomentType.zernike, 3, 20, moments_zernike_03[19]),
            Moment(MomentType.zernike, 3, 21, moments_zernike_03[20]),
            Moment(MomentType.zernike, 3, 22, moments_zernike_03[21]),
            Moment(MomentType.zernike, 3, 23, moments_zernike_03[22]),
            Moment(MomentType.zernike, 3, 24, moments_zernike_03[23]),
            Moment(MomentType.zernike, 3, 25, moments_zernike_03[24])
        ]

        self.moments = moments

        self.orientation = properties.orientation

        self.perimeter = properties.perimeter

        self.shannon_entropy = skimage.measure.shannon_entropy(properties.intensity_image)

        self.solidity = properties.solidity
