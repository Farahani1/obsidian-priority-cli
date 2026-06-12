import json
from pathlib import Path

def load_config():
    config_path = Path("_config/config.json")

    if not config_path.exists():
        raise FileNotFoundError("Missing _config/config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)