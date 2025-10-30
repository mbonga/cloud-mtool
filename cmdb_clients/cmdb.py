from typing import Any

from .base import BaseService


class CMDB(BaseService):
    """Client for CMDB REST API.

    Example:
        cmdb = CMDB('https://cmdb.example.com', auth=('user','pass'))
        cmdb._request('GET', '/api/items')
    """

    def get_item(self, item_id: str) -> Any:
        return self._request('GET', f'/items/{item_id}')
