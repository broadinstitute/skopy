import click
import skopy.command


@click.command("status")
@skopy.command.pass_context
def command(context):
    click.echo("status")
