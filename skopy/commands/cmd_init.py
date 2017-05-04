import click
import skopy.command


@click.command("init")
@skopy.command.pass_context
def command(context):
    click.echo("init")
