import base64
import logging
from typing import Any, Dict

from auth_proxy.auth_plugins.base import AuthPlugin

logger = logging.getLogger(__name__)


class BasicAuthPlugin(AuthPlugin):
    """Basic HTTP authentication plugin."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.users = config.get("users", {})

    def authenticate(self, request_headers: Dict[str, str], path: str) -> bool:
        """Authenticate using Basic auth header."""
        auth_header = request_headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            logger.debug("No Basic auth header found")
            return False

        try:
            encoded = auth_header.split(" ", 1)[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)

            if username in self.users and self.users[username] == password:
                return True

            logger.debug(f"Invalid credentials for user: {username}")
            return False
        except Exception as e:
            logger.debug(f"Basic auth parsing error: {e}")
            return False

    def get_auth_headers(
        self, request_headers: Dict[str, str], path: str
    ) -> Dict[str, str]:
        """Add username as header after successful authentication."""
        auth_header = request_headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            return {}

        try:
            encoded = auth_header.split(" ", 1)[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, _ = decoded.split(":", 1)

            return {"X-Auth-User": username}
        except Exception:
            return {}
