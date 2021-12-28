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


@cli.group(help="Show or set the current settings")
def settings():
    pass


@settings.command(help="Initialize settings")
@click.pass_context
def init(ctx):
    token = click.prompt(
        "Notion API token (from the browser cookie)",
        default=ctx.obj.settings.token or "<unset>",
    )
    page = click.prompt(
        "Notion page (from the browser location bar)",
        default=ctx.obj.settings.page or "https://notion.so/<page>",
    )

    ctx.obj.update_settings(token=token, page=page)

    click.echo(f"Settings written to {ctx.obj.settings.settings_file}")


@settings.command(help="Show the current settings")
@click.pass_context
def show(ctx):
    pprint_md(ctx.obj.settings)


@settings.command(help="Set a setting")
@click.argument("key")
@click.argument("value")
@click.pass_context
def set(ctx, key, value):
    ctx.obj.update_settings(**{key: value})
    pprint_md(ctx.obj.settings)


@cli.command(help="Run the smoke tests against a Notion URL")
@click.argument("url")
@click.pass_context
def smoke_tests(ctx, url):
    from notion.smoke_test import run_live_smoke_test

    run_live_smoke_test(ctx.settings.token, url)


if __name__ == "__main__":
    cli()
