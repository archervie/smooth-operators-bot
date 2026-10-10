import logging
import tomllib
from pathlib import Path

logger = logging.getLogger(__name__)

# Comment test_config for prod
# CONFIG_PATH = Path(__file__).parent.parent / "config.toml"
CONFIG_PATH = Path(__file__).parent.parent / "test_config.toml"
logger.info(f"Loaded config at {CONFIG_PATH}")


def config_loader() -> dict[str, str]:
    config = {}
    with open(CONFIG_PATH, mode="rb") as f:
        config: dict[str, str] = tomllib.load(f)
    return config
