"""Redact-it module."""
from typing import Any

from ruamel.yaml import YAML


class RedactIt:
    """Redact it class."""

    def __init__(self, config_file: str, file_path: str, dry_run: bool) -> None:
        """Constructor.

        :param config_file: the redact it configuration file
        :param file_path: the file path of where to glob for files
        :param dry_run: toggle on/off dry run
        """
        self.config_file: str = config_file
        self.file_path: str = file_path
        self.dry_run: bool = dry_run

        self.config: dict[str, Any] = {}

        self.yaml: YAML = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.default_flow_style = True

    def load_config_file(self) -> None:
        """Load the redact it configuration file."""
        try:
            with open(self.config_file) as f:
                self.config = self.yaml.load(f)

            if not self.config:
                print(f"Config file has no content.")
        except FileNotFoundError as e:
            print(f"Failed to load config file, error: {e}")
