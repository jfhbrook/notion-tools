import ipywidgets as widgets

from notion.ctx import Context

ctx = Context()

def get_client():
    return ctx.get_client()


def settings():
    title = widgets.Label(value="Settings")
    token_field = widgets.Password(
        description='token:',
        value=ctx.settings.token
    )
    page_field = widgets.Text(
        description='page:',
        value=ctx.settings.page
    )
    ok_button = widgets.Button(
        description='Update'
    )

    modal = widgets.VBox([
        title,
        token_field,
        page_field,
        ok_button
    ])

    def update_settings(button):
        ctx.update_settings(token=token_field.value, page=page_field.value)

    ok_button.on_click(update_settings)

    return modal
