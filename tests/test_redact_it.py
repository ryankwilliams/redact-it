import os
from collections.abc import Iterator
from typing import Any

import pytest
from ruamel.yaml import YAML

from redact_it import RedactIt


@pytest.fixture(scope="function")
def asset_file() -> Iterator[str]:
    filename: str = "file1.yml"
    yaml = YAML()
    with open(filename, "w") as f:
        yaml.dump({"foo": "bar", "secret": "secret-123"}, f)
    yield filename
    os.remove(filename)


@pytest.fixture(scope="function")
def config_file() -> Iterator[str]:
    filename: str = "redact-it.cfg"
    yaml = YAML()
    with open(filename, "w") as f:
        yaml.dump({"secret": "redacted"}, f)
    yield filename
    os.remove(filename)


@pytest.fixture(scope="function")
def redact_it_dry_run(asset_file: str, config_file: str) -> RedactIt:
    return RedactIt(config_file, True)


@pytest.fixture(scope="function")
def redact_it(asset_file: str, config_file: str) -> RedactIt:
    return RedactIt(config_file, False)


@pytest.fixture(scope="function")
def redact_it_fake_config(asset_file) -> RedactIt:
    return RedactIt("redact-it-fake.cfg", False)


@pytest.fixture(scope="function")
def redact_it_empty_config() -> Iterator[RedactIt]:
    filename: str = "redact-it-empty.cfg"
    with open(filename, "w"):
        pass
    yield RedactIt(filename, False)
    os.remove(filename)


class TestRedactIt:
    def test_no_config_file(self, redact_it_fake_config: RedactIt) -> None:
        assert redact_it_fake_config.redact() == 1

    def test_empty_config_file(self, redact_it_empty_config: RedactIt) -> None:
        assert redact_it_empty_config.redact() == 1

    def test_dry_run(self, redact_it_dry_run: RedactIt) -> None:
        assert redact_it_dry_run.redact() == 0

        with open("file1.yml") as f:
            file_content: dict[str, Any] = redact_it_dry_run.yaml.load(f)

        assert file_content["secret"] == "secret-123"

    def test_redact(self, redact_it) -> None:
        assert redact_it.redact() == 0

        with open("file1.yml") as f:
            file_content: dict[str, Any] = redact_it.yaml.load(f)

        assert file_content["secret"] == "redacted"
