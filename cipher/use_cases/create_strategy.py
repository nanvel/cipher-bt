from pathlib import Path


class CreateStrategy:
    """Create a new repository with:
    - .env
    - strategies/
    - README.md
    """

    NAME_REGEXP = r"^[\w\-]+$"

    def __init__(self, templates_root: Path):
        self.templates_root = templates_root

    def call(self, name):
        print(f"Create {name}")

    def _validate_path(self):
        pass

    def _create(self):
        pass
