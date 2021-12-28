from dataclasses import asdict, dataclass, fields, replace
import os
import os.path
from pathlib import Path
from typing import Optional

import toml


BASE_URL = "https://www.notion.so/"
API_BASE_URL = BASE_URL + "api/v3/"
SIGNED_URL_PREFIX = "https://www.notion.so/signed/"
S3_URL_PREFIX = "https://s3-us-west-2.amazonaws.com/secure.notion-static.com/"
S3_URL_PREFIX_ENCODED = "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/"

CONFIG_DIR = os.environ.get(
    "NOTION_CONFIG_DIR", str(Path(os.path.expanduser("~")) / ".config" / "notion")
)
DATA_DIR = os.environ.get(
    "NOTION_DATA_DIR", str(Path(os.path.expanduser("~")) / ".local" / "share" / "notion")
)
CACHE_DIR = str(Path(DATA_DIR) / "cache")
SETTINGS_FILE = str(Path(CONFIG_DIR) / "settings.toml")
LOG_FILE = str(Path(DATA_DIR) / "notion.log")

for dir_ in [CONFIG_DIR, DATA_DIR, CACHE_DIR]:
    os.makedirs(dir_, exist_ok=True)


class SettingsError(ValueError):
    pass


@dataclass
class Settings:
    settings_file: Path
    log_file: Path
    data_directory: Path
    token: Optional[str]
    page: Optional[str]

    @classmethod
    def from_file(cls):
        settings_file = Path(SETTINGS_FILE)
        try:
            with open(settings_file, "r") as f:
                config = toml.load(f)
        except FileNotFoundError:
            config = dict()

        return cls(
            settings_file=settings_file,
            log_file=Path(LOG_FILE),
            data_directory=Path(DATA_DIR),
            token=config.get("token", None),
            page=config.get("page", None),
        )

    def _asdict(self):
        # TODO: Better way to filter out env var sourced fields
        return {k: v for k, v in asdict(self).items() if not isinstance(v, Path)}

    def update(self, **kwargs):
        settings = replace(self, **kwargs)

        os.makedirs(self.settings_file.parent, exist_ok=True)

        with open(self.settings_file, "w") as f:
            toml.dump(settings._asdict(), f)

        return settings

    def validate(self):
        if not self.token:
            raise SettingsError("Missing notion token")
        if not self.page:
            raise SettingsError("Missing notion page")

    def _repr_markdown_(self):
        md = "## Settings\n\n"

        for field in fields(self):
            md += f"* **{field.name}**: {getattr(self, field.name) or '<unset>'}\n"

        return md
