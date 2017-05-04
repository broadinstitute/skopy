import click
import skopy.command


@click.command("foo")
@skopy.command.pass_context
def command(context):
    click.echo("foo")
