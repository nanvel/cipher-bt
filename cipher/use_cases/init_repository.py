from pathlib import Path


class InitRepository:
    """Create .env, README.md."""

    def __init__(self, templates_root: Path):
        self.templates_root = templates_root

    def call(self, path: Path):
        self._create_file_from_template(
            template_path=self.templates_root / "env.j2",
            target_path=path / ".env",
        )
        self._create_file_from_template(
            template_path=self.templates_root / "readme.j2",
            target_path=path / "README.md",
        )

    def _create_file_from_template(self, template_path: Path, target_path: Path):
        if not target_path.exists():
            with target_path.open("w", encoding="utf-8") as f:
                f.write(template_path.read_text())
