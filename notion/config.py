from dataclasses import asdict, dataclass, fields, replace
import os
import os.path
from pathlib import Path
from typing import Optional

import toml

DEFAULT_CONFIG_FILE = os.path.expanduser("~/.local/config/notion/config.toml")


class ConfigError(ValueError):
    pass


ENV_VARS = {"config_file": "NOTION_CONFIG"}


@dataclass
class Config:
    config_file: Path
    token: Optional[str]
    page: Optional[str]

    def is_stored_in_file(self, key):
        return key != "config_file"

    @classmethod
    def from_file(cls):
        config_file = Path(os.environ.get(ENV_VARS["config_file"], DEFAULT_CONFIG_FILE))
        try:
            with open(config_file, "r") as f:
                config = toml.load(f)
        except FileNotFoundError:
            config = dict()

        return cls(
            config_file=config_file,
            token=config.get("token", None),
            page=config.get("page", None),
        )

    def _asdict(self):
        return {k: v for k, v in asdict(self).items() if k not in ENV_VARS}

    def set(self, **kwargs):
        config = replace(self, **kwargs)

        os.makedirs(self.config_file.parent, exist_ok=True)

        with open(self.config_file, "w") as f:
            toml.dump(config._asdict(), f)

        return config

    def validate(self):
        if not self.token:
            raise ConfigError("Missing notion token")
        if not self.page:
            raise ConfigError("Missing notion page")

    def _repr_markdown_(self):
        md = "## Configuration\n\n"

        for field in fields(self):
            md += f"* **{field.name}**: {getattr(self, field.name) or '<unset>'}\n"

        return md
