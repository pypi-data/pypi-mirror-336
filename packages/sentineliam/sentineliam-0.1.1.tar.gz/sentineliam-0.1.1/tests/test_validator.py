from engine.validator import validate_policy
import pytest
import yaml

def test_valid_policy(tmp_path):
    file = tmp_path / "valid.yaml"
    file.write_text("action: read\nresource: db\neffect: allow")
    result = validate_policy(str(file))
    assert result.action == "read"

def test_invalid_policy(tmp_path):
    file = tmp_path / "invalid.yaml"
    file.write_text("action: read\nresource: db\neffect: unknown")
    with pytest.raises(Exception):
        validate_policy(str(file))
