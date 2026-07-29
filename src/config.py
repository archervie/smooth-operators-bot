from pathlib import Path

import tomllib

CONFIG_PATH = Path(__file__).parent.parent / "config.toml"


def config_loader() -> dict:
    with open(CONFIG_PATH, mode="rb") as f:
        config = tomllib.load(f)
    return config
