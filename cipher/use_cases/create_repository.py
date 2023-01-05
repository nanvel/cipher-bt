class CreateRepository:
    """Create a new repository with:
    - .env
    - strategies/
    - README.md
    """

    NAME_REGEXP = r"^[\w\-]+$"

    def __init__(self, root):
        self.root = root

    def call(self, name):
        name = name.strip()

        if name == ".":
            pass

    def _validate_path(self):
        pass

    def _create(self):
        pass
