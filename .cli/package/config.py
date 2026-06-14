import json
from functools import lru_cache
from pathlib import Path


class AppConfig(dict):
    @property
    def cli_dir(self) -> Path:
        return Path(self["_cli_dir"])

    @property
    def vault_path(self) -> Path:
        return Path(self["vault_path"])

    @property
    def log_dir(self) -> Path:
        return Path(self["log_dir"])

    @property
    def log_file(self) -> Path:
        return self.log_dir / "log.json"


def _cli_dir() -> Path:
    # config.py is inside: .cli/package/config.py
    return Path(__file__).resolve().parent.parent


def _resolve_path(base: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (base / path).resolve()


@lru_cache(maxsize=1)
def load_config() -> AppConfig:
    cli_dir = _cli_dir()
    config_path = cli_dir / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(f"Missing {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    config = AppConfig(raw)
    config["_cli_dir"] = str(cli_dir)

    config["vault_path"] = str(_resolve_path(cli_dir, config.get("vault_path", "..")))
    config["log_dir"] = str(_resolve_path(cli_dir, config.get("log_dir", ".")))

    config.log_dir.mkdir(parents=True, exist_ok=True)

    return config