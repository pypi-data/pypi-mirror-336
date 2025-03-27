from abc import ABC, abstractmethod
from typing import Any, Dict


class AuthPlugin(ABC):
    """Base class for authentication plugins."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def authenticate(self, request_headers: Dict[str, str], path: str) -> bool:
        """
        Authenticate a request.

        Args:
            request_headers: Headers from the incoming request
            path: The request path

        Returns:
            bool: True if authentication succeeds, False otherwise
        """
        pass

    @abstractmethod
    def get_auth_headers(
        self, request_headers: Dict[str, str], path: str
    ) -> Dict[str, str]:
        """
        Get headers to add to the authenticated request.

        Args:
            request_headers: Headers from the incoming request
            path: The request path

        Returns:
            Dict[str, str]: Headers to add to the proxied request
        """
        pass
