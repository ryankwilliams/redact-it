"""Redact it yaml module.

This module contains the core logic to redact data from yaml files.
"""
import copy
import glob
from typing import Any

from redact_it.redact_it import RedactIt


class RedactItYaml(RedactIt):
    """Redact it yaml class."""

    def __init__(self, config_file: str, file_path: str, dry_run: bool) -> None:
        """Constructor.

        :param config_file: the redact it configuration file
        :param file_path: the file path of where to glob for files
        :param dry_run: toggle on/off dry run
        """
        super().__init__(config_file, file_path, dry_run)

    def redact(self) -> int:
        """Redact data from files."""
        self.load_config_file()
        if not self.config:
            return 1

        for file in glob.glob(self.file_path, recursive=True):
            if file == self.config_file:
                continue

            try:
                with open(file) as f:
                    file_content: dict[str, Any] = self.yaml.load(f)
            except FileNotFoundError as e:
                print(f"Failed to load {file}, error: {e}")
                continue

            file_changed: bool = False

            original_file_content = copy.copy(file_content)
            file_content.update(self.config)

            if original_file_content != file_content:
                file_changed = True

            if file_changed:
                if self.dry_run:
                    print(
                        f"File {file} would be redacted, disable --dry-run to redact it"
                    )
                    continue

                print(f"Redacted {file}")

                with open(file, "w") as f:
                    self.yaml.dump(file_content, f)
        return 0
