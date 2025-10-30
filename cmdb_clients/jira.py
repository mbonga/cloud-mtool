from typing import Any, Dict

from .base import BaseService


class JIRA(BaseService):
    """Client for JIRA-like REST API.

    This is intentionally minimal — extend with real methods as needed.
    """

    def create_issue(self, project_key: str, payload: Dict[str, Any]) -> Any:
        return self._request('POST', f'/projects/{project_key}/issues', json=payload)
