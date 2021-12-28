from dataclasses import dataclass

from notion.client import NotionClient
from notion.config import Config


class Context:
    def __init__(self):
        self.config = Config.from_file()
        self._client = None

    @property
    def client(self):
        if not self._client:
            self.config.validate()
            self._client = NotionClient(token_v2=self.config.token, monitor=False)
        return self._client

    def set_config(self, **kwargs):
        self.config = self.config.set(**kwargs)
