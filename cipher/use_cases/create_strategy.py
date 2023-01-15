import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class CreateStrategy:
    NAME_REGEXP = re.compile(r"^\w+(\.py)?$")

    def __init__(self, templates_root: Path):
        self.jinja_env = Environment(loader=FileSystemLoader(templates_root))

    def call(self, name, template):
        assert self.NAME_REGEXP.match(name)

        if not name.endswith(".py"):
            name += ".py"

        target_path = Path() / name

        assert not target_path.exists()

        with target_path.open("w", encoding="utf-8") as f:
            f.write(
                self.jinja_env.get_template(f"strategies/{template}.j2").render(
                    class_name=self._name_to_class_name(name[:-3])
                )
                + "\n"
            )

    def _name_to_class_name(self, name: str) -> str:
        class_name = "".join(
            [(i[0].isupper() and i or i.capitalize()) for i in name.split("_")]
        )
        if not class_name.endswith("Strategy"):
            class_name += "Strategy"
        return class_name
