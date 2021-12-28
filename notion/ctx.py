from notion.client import NotionClient
from notion.settings import Settings


class Context:
    def __init__(self):
        self.settings = Settings.from_file()
        self._client = None

    def get_client(self):
        if not self._client:
            self.settings.validate()
            self._client = NotionClient(token_v2=self.settings.token, monitor=False)
        return self._client

    def update_settings(self, **kwargs):
        self.settings = self.settings.update(**kwargs)
