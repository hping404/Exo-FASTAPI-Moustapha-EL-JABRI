import json
import logging
import pathlib
from models import Server

logger = logging.getLogger(__name__)


class ConfigError(ValueError):
    pass


class ConfigLoader:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)

    def load(self) -> list[Server]:
        logger.info("Loading config from %s", self.path)

        try:
            raw = json.loads(self.path.read_text())
        except FileNotFoundError:
            raise ConfigError(f"File not found: {self.path}")
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON: {e}") from e

        servers: list[Server] = []

        for i, entry in enumerate(raw, start=1):
            servers.append(
                Server(
                    id=i,
                    name=entry["name"],
                    host=entry["host"],
                    port=entry["port"],
                    protocol=entry.get("protocol", "http"),
                    health_path=entry.get("health_path", "/health"),
                )
            )

        logger.info("Loaded %d servers", len(servers))
        return servers
