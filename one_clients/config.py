import json
import os
from typing import Any, Dict, Optional

from .singleton import SingletonMeta


def _cast_value(value: Any, to_type: str) -> Any:
    if value is None:
        return None
    if to_type in (None, 'str'):
        return str(value)
    if to_type == 'int':
        return int(value)
    if to_type == 'float':
        return float(value)
    if to_type == 'bool':
        if isinstance(value, bool):
            return value
        v = str(value).lower()
        if v in ('1', 'true', 'yes', 'on'):
            return True
        if v in ('0', 'false', 'no', 'off'):
            return False
        raise ValueError(f'Cannot cast {value!r} to bool')
    if to_type == 'json':
        if isinstance(value, (dict, list)):
            return value
        return json.loads(value)
    # fallback
    return value


class Config(metaclass=SingletonMeta):
    """Configuration container with schema, environment mapping and secrets.

    Schema format (example):
      {
          'CMDB_URL': {'env': 'CMDB_URL', 'type': 'str', 'default': 'https://...', 'secret': False},
          'TIMEOUT': {'env': 'TIMEOUT', 'type': 'int', 'default': 30}
      }

    Behavior:
    - Values are taken from explicit loaded data (via load_dict/load_file) first.
    - Then environment variables are consulted using the `env` name if provided or the key name.
    - Values may be typed according to schema.
    - If a value starts with `file://` it will be read from the referenced file (useful for secrets mounted as files).
    - `as_dict(mask_secrets=True)` will mask secret values.
    """

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self._schema: Dict[str, Dict[str, Any]] = {}

    def set_schema(self, schema: Dict[str, Dict[str, Any]]) -> None:
        """Register a schema describing expected keys and their types/env mappings."""
        self._schema = dict(schema)

    def load_dict(self, data: Dict[str, Any]) -> None:
        self._data.update(data)

    def load_file(self, path: str) -> None:
        path = os.path.expanduser(path)
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError('Config file must contain a JSON object (dict)')
        self._data.update(data)

    def _resolve_file_secret(self, val: str) -> str:
        # file://path or file:///absolute/path
        if not isinstance(val, str):
            return val
        if not val.startswith('file://'):
            return val
        path = val[len('file://'):]
        path = os.path.expanduser(path)
        with open(path, 'r', encoding='utf-8') as fh:
            return fh.read().strip()

    def _get_from_env(self, key: str) -> Optional[str]:
        entry = self._schema.get(key, {})
        env_name = entry.get('env', key)
        return os.environ.get(env_name)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value applying schema typing and env-var mapping.

        Precedence: explicit data loaded via load_dict/load_file -> environment -> schema default -> provided default
        """
        # explicit
        if key in self._data:
            val = self._data[key]
        else:
            # try env
            env_val = self._get_from_env(key)
            if env_val is not None:
                val = env_val
            else:
                # schema default
                val = self._schema.get(key, {}).get('default', default)

        # resolve file-based secret if applicable
        try:
            val = self._resolve_file_secret(val) if isinstance(val, str) else val
        except FileNotFoundError:
            # fall back to original val
            pass

        # cast according to schema
        cast_to = self._schema.get(key, {}).get('type')
        if cast_to:
            try:
                return _cast_value(val, cast_to)
            except Exception:
                # if cast fails, raise a helpful error
                raise
        return val

    def as_dict(self, mask_secrets: bool = False) -> Dict[str, Any]:
        out = dict(self._data)
        # include schema defaults/envs if missing
        for key, entry in self._schema.items():
            if key not in out:
                try:
                    out[key] = self.get(key)
                except Exception:
                    out[key] = None

        if mask_secrets:
            for key, entry in self._schema.items():
                if entry.get('secret') and key in out:
                    out[key] = '*****'
        return out
