from cipher.models import Template

from .. import DATA_PATH


def test_template():
    members = [t.value for t in Template]

    for member in members:
        assert (DATA_PATH / f"../../cipher/templates/strategies/{member}.j2").is_file()
