from dataclasses import fields
import click
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import MarkdownLexer

from notion.ctx import Context


def pprint_md(obj):
    print(highlight(obj._repr_markdown_(), MarkdownLexer(), Terminal256Formatter()))


class TasksType(click.ParamType):
    name = "task"

    def convert(self, value, param, ctx):
        try:
            return [int(task) for task in value.split(",")]
        except ValueError:
            self.fail(f"{value!r} not a comma-separated list of integers", param, ctx)


TASKS = TasksType()


@click.group(help="A Notion.so CLI focused on simple task management")
@click.pass_context
def cli(ctx):
    ctx.ensure_object(Context)


@cli.group(help="Show or set the current configuration")
def config():
    pass


@config.command(help="Initialize the configuration")
@click.pass_context
def init(ctx):
    token = click.prompt(
        "Notion API token (from the browser cookie)",
        default=ctx.obj.config.token or "<unset>",
    )
    page = click.prompt(
        "Notion page (from the browser location bar)",
        default=ctx.obj.config.page or "https://notion.so/<page>",
    )

    ctx.obj.set_config(token=token, page=page)

    click.echo(f"Configuration written to {config.config_file}")


@config.command(help="Show the current configuration")
@click.pass_context
def show(ctx):
    pprint_md(ctx.obj.config)


@config.command(help="Set a configuration field")
@click.argument("key")
@click.argument("value")
@click.pass_context
def set(ctx, key, value):
    ctx.obj.set_config(**{key: value})
    pprint_md(ctx.obj.config)


if __name__ == "__main__":
    cli()
