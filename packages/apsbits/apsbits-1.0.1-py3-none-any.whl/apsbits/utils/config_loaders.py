"""
Configuration management for the instrument.

This module serves as the single source of truth for instrument configuration.
It loads and validates the configuration from the iconfig.yml file and provides
access to the configuration throughout the application.
"""

import logging
import pathlib
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

import tomli  # type: ignore
import yaml

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Global configuration instance
_iconfig: Dict[str, Any] = {}


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML or TOML file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        The loaded configuration dictionary.

    Raises:
        ValueError: If config_path is None or if the file extension is not supported.
        FileNotFoundError: If the configuration file does not exist.
    """
    global _iconfig

    if config_path is None:
        raise ValueError("config_path must be provided")

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    try:
        with open(config_path, "rb") as f:
            if config_path.suffix.lower() == ".yml":
                config = yaml.safe_load(f)
            elif config_path.suffix.lower() == ".toml":
                config = tomli.load(f)
            else:
                raise ValueError(
                    f"Unsupported configuration file format: {config_path.suffix}"
                )

            if config is None:
                config = {}
            _iconfig.update(config)

            _iconfig["ICONFIG_PATH"] = str(config_path)
            _iconfig["INSTRUMENT_PATH"] = str(config_path.parent)
            _iconfig["INSTRUMENT_FOLDER"] = str(config_path.parent.name)

            return _iconfig
    except Exception as e:
        logger.error("Error loading configuration: %s", e)
        raise


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration.

    Returns:
        The current configuration dictionary.
    """
    return _iconfig


def update_config(updates: Dict[str, Any]) -> None:
    """
    Update the current configuration.

    Args:
        updates: Dictionary of configuration updates.
    """
    _iconfig.update(updates)


def load_config_yaml(config_obj) -> dict:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        The loaded configuration dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """

    if config_obj is None:
        raise ValueError("config_path must be provided")

    try:
        # If it's a path, open it first
        if isinstance(config_obj, (str, pathlib.Path)):
            with open(config_obj, "r") as f:
                content = f.read()
        # Otherwise assume it's a file-like object
        else:
            content = config_obj.read()

        iconfig = yaml.load(content, yaml.Loader)
        return iconfig
    except Exception as e:
        logger.error("Error loading configuration: %s", e)
        raise
