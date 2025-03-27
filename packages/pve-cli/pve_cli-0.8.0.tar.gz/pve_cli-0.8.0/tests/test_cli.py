from pathlib import Path

import pytest
from typer import BadParameter
from typer.testing import CliRunner

from pve_cli import __version__
from pve_cli.main import cli
from pve_cli.util.validators import endpoint_validate

ERROR_CODE_INVALID_CLUSTER = 2


class TestCLIMain:
    def test_version(self, runner: CliRunner):
        result = runner.invoke(cli, ['--version'])

        assert result.exit_code == 0
        assert __version__ in result.stdout


class TestCLIClusterArgument:
    # def test_valid_cluster(self, runner: CliRunner, valid_config_no_default_cluster: Path):
    #     result = runner.invoke(cli, ['--config', valid_config_no_default_cluster, '-C', 'examplecluster'])
    #     print(result.stdout)
    #     assert result.exit_code == 0

    def test_invalid_endpoint(self, runner: CliRunner, valid_config_file: Path):
        result = runner.invoke(cli, ['--config', valid_config_file, '--endpoint', 'invalidcluster'])
        assert result.exit_code == ERROR_CODE_INVALID_CLUSTER
        assert 'invalidcluster' in result.stdout


class TestValidateCluster:
    def test_valid_cluster(self, valid_config: dict):
        try:
            endpoint_validate(valid_config, 'examplecluster')
        except Exception as exc:
            pytest.fail(f'validate_cluster raised exception {exc}')

    def test_invalid_cluster(self, valid_config: dict):
        with pytest.raises(BadParameter):
            endpoint_validate(valid_config, 'invalidcluster')
