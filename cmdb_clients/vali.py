from typing import Any, Dict

from .base import BaseService


class VALI(BaseService):
    """Client for VALI REST API.

    This follows the same pattern as CMDB.
    """

    def validate(self, payload: Dict[str, Any]) -> Any:
        return self._request('POST', '/validate', json=payload)
