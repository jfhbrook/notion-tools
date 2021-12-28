from notion.ctx import Context

ctx = Context()
settings = ctx.settings


def get_client():
    return ctx.get_client()
