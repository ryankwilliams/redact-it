"""Pytest conftest module."""
import os
from collections.abc import Iterator

import pytest
from ruamel.yaml import YAML


@pytest.fixture(scope="function")
def asset_file() -> Iterator[str]:
    filename: str = "file1.yml"
    yaml = YAML()
    with open(filename, "w") as f:
        yaml.dump(
            {
                "foo": "bar",
                "secret": "secret-123",
                "apple": {"recipe": "secret-recipe"},
            },
            f,
        )
    yield filename
    os.remove(filename)


@pytest.fixture(scope="function")
def config_file() -> Iterator[str]:
    filename: str = "redact-it.cfg"
    yaml = YAML()
    with open(filename, "w") as f:
        yaml.dump(
            {"secret": "redacted", "apple": {"recipe": "redacted"}},
            f,
        )
    yield filename
    os.remove(filename)
