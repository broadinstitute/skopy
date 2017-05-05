# -*- coding: utf-8 -*-

import click
import itertools
import numpy
import pandas
import scipy.stats
import skimage.io
import skimage.measure
import skopy.command


@click.command("compare")
@click.argument("images", nargs=-1, type=click.Path(exists=True))
@skopy.command.pass_context
def command(context, images):
    """

    """
    columns = [
        "mse",
        "nrmse",
        "pcc",
        "psnr",
        "ssim",
        "x",
        "y"
    ]

    records = []

    for x_pathname, y_pathname in itertools.combinations(images, 2):
        x_image = skimage.io.imread(x_pathname)
        y_image = skimage.io.imread(y_pathname)

        record = [
            skimage.measure.compare_mse(x_image, y_image),
            skimage.measure.compare_nrmse(x_image, y_image),
            numpy.corrcoef(x_image, y_image)[0, 1],
            skimage.measure.compare_psnr(x_image, y_image),
            skimage.measure.compare_ssim(x_image, y_image),
            x_pathname,
            y_pathname
        ]

        records.append(record)

    measurements = pandas.DataFrame(data=records, columns=columns)

    click.echo(measurements)
