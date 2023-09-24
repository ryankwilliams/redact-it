import os
from collections.abc import Iterator
from typing import Any

import pytest

from redact_it.redact_yaml import RedactItYaml


@pytest.fixture(scope="function")
def redact_it_yaml_dry_run(asset_file: str, config_file: str) -> RedactItYaml:
    return RedactItYaml(config_file, asset_file, True)


@pytest.fixture(scope="function")
def redact_it_yaml(asset_file: str, config_file: str) -> RedactItYaml:
    return RedactItYaml(config_file, asset_file, False)


@pytest.fixture(scope="function")
def redact_it_yaml_fake_config(asset_file: str) -> RedactItYaml:
    return RedactItYaml("redact-it-fake.cfg", asset_file, False)


@pytest.fixture(scope="function")
def redact_it_yaml_empty_config() -> Iterator[RedactItYaml]:
    filename: str = "redact-it-empty.cfg"
    with open(filename, "w"):
        pass
    yield RedactItYaml(filename, "**/*.yml", False)
    os.remove(filename)


class TestRedactIt:
    def test_no_config_file(self, redact_it_yaml_fake_config: RedactItYaml) -> None:
        assert redact_it_yaml_fake_config.redact() == 1

    def test_empty_config_file(self, redact_it_yaml_empty_config: RedactItYaml) -> None:
        assert redact_it_yaml_empty_config.redact() == 1

    def test_dry_run(self, redact_it_yaml_dry_run: RedactItYaml) -> None:
        assert redact_it_yaml_dry_run.redact() == 0

        with open("file1.yml") as f:
            file_content: dict[str, Any] = redact_it_yaml_dry_run.yaml.load(f)

        assert file_content["secret"] == "secret-123"

    def test_redact(self, redact_it_yaml: RedactItYaml) -> None:
        assert redact_it_yaml.redact() == 0

        with open("file1.yml") as f:
            file_content: dict[str, Any] = redact_it_yaml.yaml.load(f)

        assert file_content["secret"] == "redacted"
