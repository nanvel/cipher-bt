from pathlib import Path


class InitRepository:
    """Create .env."""

    def __init__(self, templates_root: Path):
        self.templates_root = templates_root

    def call(self, path: Path):
        dot_env_path = path / ".env"
        if not dot_env_path.exists():
            with dot_env_path.open("w", encoding="utf-8") as f:
                f.write((self.templates_root / "env.j2").read_text())
