import base64
import logging
from typing import Any, Dict

from .base import AuthPlugin, AuthResult

logger = logging.getLogger(__name__)


class BasicAuthPlugin(AuthPlugin):
    """Basic HTTP authentication plugin."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.users = config.get("users", {})
        self.realm = config.get("realm", "Authentication Required")

    def authenticate(self, request_headers: Dict[str, str], path: str) -> AuthResult:
        """Authenticate using Basic auth header."""
        auth_header = request_headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            logger.debug("No Basic auth header found")
            # Return a challenge to the client
            return AuthResult(
                authenticated=False,
                headers={"WWW-Authenticate": f'Basic realm="{self.realm}"'},
            )

        try:
            encoded = auth_header.split(" ", 1)[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)

            if username in self.users and self.users[username] == password:
                # Authentication successful
                auth_headers = self.get_auth_headers(request_headers, path)
                return AuthResult(authenticated=True, headers=auth_headers)

            logger.debug(f"Invalid credentials for user: {username}")
            # Return a challenge to the client
            return AuthResult(
                authenticated=False,
                headers={"WWW-Authenticate": f'Basic realm="{self.realm}"'},
            )
        except Exception as e:
            logger.debug(f"Basic auth parsing error: {e}")
            # Return a challenge to the client
            return AuthResult(
                authenticated=False,
                headers={"WWW-Authenticate": f'Basic realm="{self.realm}"'},
            )

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
