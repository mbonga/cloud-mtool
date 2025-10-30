from typing import Any, Dict, Optional

from .singleton import SingletonMeta


class BaseService(metaclass=SingletonMeta):
    """Minimal HTTP REST API service using requests.

    Network calls import `requests` inside the method so importing this module
    doesn't require `requests` to be installed until you actually call the API.
    """

    def __init__(self, base_url: str, auth: Optional[Any] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.auth = auth
        self.timeout = timeout

    def _request(self, method: str, path: str, **kwargs) -> Any:
        # Import locally so package import doesn't require requests immediately
        import requests

        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)
        if self.auth:
            kwargs.setdefault('auth', self.auth)

        resp = requests.request(method, url, **kwargs)
        resp.raise_for_status()

        # Try to return json if possible, otherwise text
        try:
            return resp.json()
        except ValueError:
            return resp.text
