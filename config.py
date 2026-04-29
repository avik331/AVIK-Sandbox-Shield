import yaml
import secrets
import os
from pathlib import Path
from typing import Any


class Config:
    def __init__(self, path: str = "config.yaml"):
        self._data = self._load(path)

    def _load(self, path: str) -> dict:
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"{path} not found. Please create it from the template.")
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]


# Global singleton
config = Config()


def load_config(config_path: str = "config.yaml", **_kwargs) -> Config:
    """Return the global Config instance, or a new one if a custom path is given."""
    global config
    if config_path != "config.yaml":
        config = Config(config_path)
    return config


def load_key(cfg: Config, key_type: str) -> bytes:
    """
    Load a cryptographic key from the path defined in config.yaml.

    key_type: "master" or "killswitch"
    Falls back to ~/.avik/keys if the primary path is not writable.
    """
    key_map = {
        "master":      "master_key_file",
        "killswitch":  "killswitch_key_file",
    }
    field = key_map.get(key_type)
    if field is None:
        raise ValueError(f"Unknown key type: {key_type!r}")

    keys_cfg = cfg.get("keys", {})
    primary_path = Path(keys_cfg.get(field, f"/etc/avik/keys/{key_type}.key"))
    fallback_dir = Path(os.path.expanduser(keys_cfg.get("fallback_dir", "~/.avik/keys")))

    if primary_path.exists():
        return primary_path.read_bytes()

    # Auto-generate and store under fallback directory
    fallback_path = fallback_dir / primary_path.name
    if fallback_path.exists():
        return fallback_path.read_bytes()

    fallback_dir.mkdir(parents=True, exist_ok=True)
    key = secrets.token_bytes(32)
    fallback_path.write_bytes(key)
    os.chmod(fallback_path, 0o600)
    return key