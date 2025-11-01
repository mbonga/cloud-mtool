from typing import Any, Dict, List

from .base import BaseService


class JIRA(BaseService):
    """Client for JIRA-like REST API.

    This is intentionally minimal — extend with real methods as needed.
    """

    def create_issue(self, project_key: str, payload: Dict[str, Any]) -> Any:
        return self._request('POST', f'/projects/{project_key}/issues', json=payload)

    def jql(self, query: str, path: str = '/search') -> List[str]:
        """Run a JQL query and return a list of issue keys.

        This calls the service's search endpoint with the provided JQL string
        and returns the found issue keys as a list of strings. It expects the
        API to return JSON with an `issues` array where each issue has a
        `key` attribute (standard JIRA API). If the response is a plain
        list of strings, it will be returned directly.
        """
        # Allow overriding the REST path (some JIRA instances use /rest/api/2/search)
        resp = self._request('GET', path, params={'jql': query})

        # If response is a mapping with 'issues', extract keys
        if isinstance(resp, dict) and 'issues' in resp:
            issues = resp.get('issues') or []
            keys: List[str] = []
            for it in issues:
                if isinstance(it, dict) and 'key' in it:
                    keys.append(str(it['key']))
                else:
                    # If the item is already a string, accept it
                    if isinstance(it, str):
                        keys.append(it)
            return keys

        # If it's already a list of strings, return as-is (cast)
        if isinstance(resp, list):
            return [str(x) for x in resp]

        # Unknown shape, return empty list
        return []
