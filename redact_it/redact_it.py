"""Redact-it module."""
import argparse
import glob
from collections.abc import Sequence
from typing import Any

from ruamel.yaml import YAML


class RedactIt:
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
                    file_content: Any = self.yaml.load(f)
            except FileNotFoundError as e:
                print(f"Failed to load {file}, error: {e}")
                continue

            count: int = 0

            for key, value in self.config.items():
                if key in file_content and file_content[key] != value:
                    file_content[key] = value
                    count += 1

            if count > 0:
                if self.dry_run:
                    print(
                        f"File {file} would be redacted, disable --dry-run to redact it"
                    )
                    continue

                print(f"Redacted {file}")

                with open(file, "w") as f:
                    self.yaml.dump(file_content, f)

        return 0


def main(argv: Sequence[str] | None = None) -> int:
    """redact-it"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config")
    parser.add_argument("-fp", "--file-path", dest="file_path")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true")
    args = parser.parse_args(argv)

    if not args.config:
        print(
            "No redact-it configuration file provided, pass one "
            "`-c or--config` and try again."
        )
        return 1

    redact_it: RedactIt = RedactIt(args.config, args.file_path, args.dry_run)
    return redact_it.redact()


if __name__ == "__main__":
    raise SystemExit(main())
