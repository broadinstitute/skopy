import click
import skimage.io
import skopy.preprocessing.image


@click.command("label")
@click.argument("a", nargs=1, type=click.Path(exists=True))
@click.argument("b", nargs=1, type=click.Path(exists=True))
def command(a, b):
    x = skimage.io.imread(a)
    y = skimage.io.imread(b)

    x, y = skopy.preprocessing.image.label(x, y)

    skimage.io.imsave(a, x)
    skimage.io.imsave(b, y)
