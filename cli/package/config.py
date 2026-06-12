import json
from pathlib import Path

def load_config():
    config_file = "./cli/config.json"

    config_path = Path(config_file)

    if not config_path.exists():
        raise FileNotFoundError("Missing "+config_file)

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)