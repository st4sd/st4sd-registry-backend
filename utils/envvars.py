import os
from typing import Dict


def get_settings_env_vars() -> Dict[str, str]:
    env_vars = os.environ
    settings_env_vars = {}

    for k in env_vars.keys():
        if k.startswith("ST4SD_REGISTRY_UI_SETTINGS_"):
            settings_env_vars[k] = os.environ[k]

    return settings_env_vars


def is_global_registry() -> bool:
    return os.getenv("ST4SD_REGISTRY_UI_SETTINGS_IS_GLOBAL", "no") == "yes"
