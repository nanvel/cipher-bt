import re

from pathlib import Path


class CreateStrategy:
    NAME_REGEXP = re.compile(r"^\w+$")

    def __init__(self, templates_root: Path):
        self.templates_root = templates_root

    def call(self, name, template):
        assert self.NAME_REGEXP.match(name)
        template_path = self.templates_root / "strategies" / (template + ".j2")
        target_path = Path() / (name + ".py")

        assert not target_path.exists()

        with target_path.open("w", encoding="utf-8") as f:
            f.write(template_path.read_text())
