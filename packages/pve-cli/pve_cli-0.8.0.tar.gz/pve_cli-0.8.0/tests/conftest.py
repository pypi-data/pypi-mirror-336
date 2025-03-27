from pathlib import Path

import pytest
import toml
from typer.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def valid_config() -> dict:
    return {
        'defaults': {'endpoint': 'examplecluster'},
        'endpoint': {
            'examplecluster': {
                'host': 'examplehost',
                'user': 'root',
                'realm': 'foo',
                'token_name': 'test',
                'token_secret': 'PSSST!',
            }
        },
    }


@pytest.fixture
def valid_config_file(tmp_path: Path, valid_config: dict) -> Path:
    config_file_path = tmp_path / 'config.toml'
    config = valid_config
    config_file_path.write_text(toml.dumps(config))
    return config_file_path


@pytest.fixture
def invalid_config_invalid_endpoint() -> dict:
    return {
        'defaults': {'endpoint': 'invalid'},
        'endpoint': {
            'examplecluster': {
                'host': 'examplehost',
                'user': 'root',
                'realm': 'foo',
                'token_name': 'test',
                'token_secret': 'PSSST!',
            }
        },
    }


@pytest.fixture
def invalid_config_missing_keys() -> dict:
    return {
        'defaults': {'endpoint': 'examplecluster'},
        'endpoint': {
            'examplecluster': {'host': 'examplehost', 'user': 'root', 'token_name': 'test', 'token_secret': 'PSSST!'},
            'second_cluster': {'host': 'host2', 'token_name': 'test', 'token_secret': 'PSSST!'},
        },
    }
