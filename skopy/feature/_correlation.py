# -*- coding: utf-8 -*-

import skimage.io
import skimage.measure
import sqlalchemy

from ._base import Base


class Correlation(Base):
    __tablename__ = "correlations"

    x_pathname = sqlalchemy.Column(sqlalchemy.String)
    y_pathname = sqlalchemy.Column(sqlalchemy.String)

    mean_squared_error = sqlalchemy.Column(sqlalchemy.Float)

    normalized_root_mean_square_deviation = sqlalchemy.Column(sqlalchemy.Float)

    peak_signal_to_noise_ratio = sqlalchemy.Column(sqlalchemy.Float)

    structural_similarity = sqlalchemy.Column(sqlalchemy.Float)

    def __init__(self, x, y):
        self.x_pathname = x
        self.y_pathname = y

        x = skimage.io.imread(x)
        y = skimage.io.imread(y)

        self.mean_squared_error = skimage.measure.compare_mse(x, y)

        self.normalized_root_mean_square_deviation = skimage.measure.compare_nrmse(x, y)

        self.peak_signal_to_noise_ratio = skimage.measure.compare_psnr(x, y)

        self.structural_similarity = skimage.measure.compare_ssim(x, y)
