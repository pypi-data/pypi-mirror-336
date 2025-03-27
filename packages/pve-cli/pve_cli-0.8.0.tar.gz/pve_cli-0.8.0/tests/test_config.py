import pytest

from pve_cli.util.exceptions import InvalidConfigError
from pve_cli.util.validators import config_validate


class TestValidateConfig:
    def test_valid_config(self, valid_config: dict):
        try:
            config_validate(valid_config)
        except Exception as exc:
            pytest.fail(f'validate_config raised exception {exc}')

    def test_invalid_default_endpoint(self, invalid_config_invalid_endpoint: dict):
        with pytest.raises(InvalidConfigError):
            config_validate(invalid_config_invalid_endpoint)

    def test_missing_cluster_key(self, invalid_config_missing_keys: dict):
        with pytest.raises(InvalidConfigError) as exc:
            config_validate(invalid_config_missing_keys)

        assert 'examplecluster: realm' in str(exc.value)
        assert 'second_cluster: user, realm' in str(exc.value)
