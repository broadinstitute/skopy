import os
import sys

import click


class Command(click.MultiCommand):
    def list_commands(self, context):
        rv = []

        commands = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))

        for filename in os.listdir(commands):
            if filename.endswith(".py") and filename.startswith("command_"):
                _, name = filename.split("command_")

                name, _ = name.split(".py")

                rv.append(name)

        rv.sort()

        return rv

    def get_command(self, context, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")

            name = "skopy.commands.command_" + name

            mod = __import__(name, None, None, ["command"])
        except ImportError:
            return

        return mod.command


class Context:
    def __init__(self):
        self.image = None


context_settings = {"auto_envvar_prefix": "SKOPY"}

pass_context = click.make_pass_decorator(Context, ensure=True)


@click.command("command", Command, context_settings=context_settings)
@pass_context
def command(context):
    pass
