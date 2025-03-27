import asyncio
import logging
import re
import socket
from typing import Any, Dict, List, Optional, Set, Tuple

import aiohttp

from auth_proxy.auth_plugins import create_plugin_instance
from auth_proxy.auth_plugins.base import AuthPlugin

logger = logging.getLogger(__name__)


class AuthProxy:
    """Authenticating reverse proxy."""

    def __init__(self, config: Dict):
        self.config = config

        # Load all configured plugins
        self.auth_plugins = {}
        plugins_config = config.get("auth_plugins", {})

        for plugin_name, plugin_config in plugins_config.items():
            try:
                self.auth_plugins[plugin_name] = create_plugin_instance(
                    plugin_name, plugin_config
                )
                logger.info(f"Loaded authentication plugin instance: {plugin_name}")
            except Exception as e:
                logger.error(f"Failed to load plugin instance {plugin_name}: {e}")

        # Global auth settings
        self.auth_config = config.get("auth", {})
        self.default_plugins = self.auth_config.get("default_plugins", [])
        self.default_mode = self.auth_config.get("default_mode", "any")

        # Backend configuration (with defaults)
        backend = config.get("backend", {})
        self.backend_scheme = backend.get("scheme", "http")
        self.backend_host = backend.get("host", "localhost")
        self.backend_port = backend.get("port", 3000)  # Default port
        self.backend_socket = backend.get("socket")

        # Path rules - precompile regex patterns
        self.paths = []
        for path_rule in config.get("paths", []):
            if path_rule.get("regex", False):
                try:
                    pattern = re.compile(path_rule["path"])
                    self.paths.append({**path_rule, "pattern": pattern})
                except re.error as e:
                    logger.error(f"Invalid regex pattern '{path_rule['path']}': {e}")
            else:
                self.paths.append(path_rule)

    def _get_path_rule(self, path: str) -> Dict:
        """
        Find the matching path rule for a given path.

        Args:
            path: The request path

        Returns:
            Dict: The matching path rule, or a default rule if no match
        """
        # Process rules in order (as defined in the config)
        for path_rule in self.paths:
            if "pattern" in path_rule:  # Regex pattern
                if path_rule["pattern"].match(path):
                    return path_rule
            else:  # Simple prefix matching
                pattern = path_rule.get("path", "")
                if path.startswith(pattern):
                    return path_rule

        # No matching rule found, use default behavior
        default_behavior = self.auth_config.get("default_behavior", "authenticated")
        authenticate = default_behavior == "authenticated"

        # Create a default rule
        return {
            "authenticate": authenticate,
            "plugins": self.default_plugins if authenticate else [],
            "mode": self.default_mode,
        }

    async def _authenticate_request(
        self, headers: Dict[str, str], path: str, path_rule: Dict
    ) -> Tuple[bool, Dict[str, str]]:
        """
        Authenticate a request using the specified plugins.

        Args:
            headers: The request headers
            path: The request path
            path_rule: The matching path rule

        Returns:
            Tuple[bool, Dict[str, str]]: (authenticated, auth_headers)
        """
        # If authentication is not required, return success
        if not path_rule.get("authenticate", True):
            return True, {}

        # Get the plugins to use
        plugin_names = path_rule.get("plugins", self.default_plugins)
        if not plugin_names:
            # No plugins specified and no defaults
            logger.warning(
                f"No authentication plugins specified for path '{path}' and no defaults configured"
            )
            return False, {}

        # Get the authentication mode
        mode = path_rule.get("mode", self.default_mode)

        # Collect authentication results and headers
        auth_results = []
        all_auth_headers = {}

        for plugin_name in plugin_names:
            auth_plugin = self.auth_plugins.get(plugin_name)
            if not auth_plugin:
                logger.error(
                    f"Authentication plugin '{plugin_name}' specified but not loaded"
                )
                continue

            # Attempt authentication
            authenticated = auth_plugin.authenticate(headers, path)
            auth_results.append(authenticated)

            # If authenticated, collect headers
            if authenticated:
                auth_headers = auth_plugin.get_auth_headers(headers, path)
                all_auth_headers.update(auth_headers)

        # Determine overall authentication result
        if mode == "all":
            # All plugins must succeed
            authenticated = all(auth_results) if auth_results else False
            # If not authenticated, clear the headers
            if not authenticated:
                all_auth_headers = {}
        else:
            # Any plugin can succeed (default)
            authenticated = any(auth_results) if auth_results else False

        return authenticated, all_auth_headers

    async def handle_request(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """
        Handle an incoming HTTP request.

        Args:
            reader: Stream reader for the client connection
            writer: Stream writer for the client connection
        """
        try:
            # Parse the HTTP request
            request_line_in = await reader.readline()
            if not request_line_in:
                return

            request_line = request_line_in.decode("utf-8").strip()
            logger.debug(f"Request line: {request_line}")
            method, path, protocol = request_line.split(" ")

            # Read headers
            headers = {}
            while True:
                header_line_in = await reader.readline()
                header_line = header_line_in.decode("utf-8").strip()
                if not header_line:
                    break

                key, value = header_line.split(":", 1)
                headers[key.strip()] = value.strip()

            logger.debug(f"Request headers: {headers}")

            # Read body if present
            content_length = int(headers.get("Content-Length", "0"))
            body = await reader.read(content_length) if content_length else b""

            # Get the matching path rule
            path_rule = self._get_path_rule(path)
            logger.debug(f"Matching path rule: {path_rule}")

            # Authenticate the request
            authenticated, auth_headers = await self._authenticate_request(
                headers, path, path_rule
            )
            logger.debug(
                f"Authentication result: {authenticated}, headers: {auth_headers}"
            )

            # Update headers with authentication information
            if authenticated:
                headers.update(auth_headers)
            else:
                # Send 401 Unauthorized response
                logger.debug("Sending 401 Unauthorized response")
                writer.write(b"HTTP/1.1 401 Unauthorized\r\n")
                writer.write(b"Content-Type: text/plain\r\n")
                writer.write(b"Content-Length: 12\r\n")
                writer.write(b"\r\n")
                writer.write(b"Unauthorized")
                await writer.drain()
                return  # Return without closing the writer, it will be closed in the finally block

            # Forward the request to the backend
            try:
                logger.debug(f"Forwarding request to backend")
                async with aiohttp.ClientSession() as session:
                    # Construct backend URL
                    if self.backend_socket:
                        # Unix socket
                        connector = aiohttp.UnixConnector(path=self.backend_socket)
                        backend_url = f"{self.backend_scheme}://localhost{path}"
                        client_kwargs = {"connector": connector}
                    else:
                        # TCP socket
                        backend_url = f"{self.backend_scheme}://{self.backend_host}"
                        if self.backend_port:
                            backend_url += f":{self.backend_port}"
                        backend_url += path
                        client_kwargs = {}

                    logger.debug(f"Backend URL: {backend_url}")

                    # Forward the request
                    async with session.request(
                        method, backend_url, headers=headers, data=body, **client_kwargs
                    ) as response:
                        # Write response status line
                        status_line = (
                            f"HTTP/1.1 {response.status} {response.reason}\r\n"
                        )
                        logger.debug(f"Backend response: {status_line.strip()}")
                        writer.write(status_line.encode())

                        # Write response headers
                        for key, value in response.headers.items():
                            header_line = f"{key}: {value}\r\n"
                            writer.write(header_line.encode())

                        # End headers
                        writer.write(b"\r\n")

                        # Stream response body
                        async for chunk in response.content.iter_chunked(8192):
                            writer.write(chunk)

                        await writer.drain()
            except Exception as e:
                logger.error(f"Error forwarding request to backend: {e}")
                # Send 502 Bad Gateway
                writer.write(b"HTTP/1.1 502 Bad Gateway\r\n")
                writer.write(b"Content-Type: text/plain\r\n")
                writer.write(b"Content-Length: 11\r\n")
                writer.write(b"\r\n")
                writer.write(b"Bad Gateway")
                await writer.drain()
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            try:
                # Send 500 Internal Server Error
                writer.write(b"HTTP/1.1 500 Internal Server Error\r\n")
                writer.write(b"Content-Type: text/plain\r\n")
                writer.write(b"Content-Length: 21\r\n")
                writer.write(b"\r\n")
                writer.write(b"Internal Server Error")
                await writer.drain()
            except:
                pass
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass

    async def start(self) -> None:
        """Start the proxy server."""
        listen_config = self.config.get("listen", {})
        host = listen_config.get("host", "127.0.0.1")
        port = listen_config.get("port")
        socket_path = listen_config.get("socket")

        if socket_path:
            # Unix socket server
            server = await asyncio.start_unix_server(
                self.handle_request, path=socket_path
            )
            logger.info(f"Proxy server listening on Unix socket {socket_path}")
        elif port:
            # TCP server
            server = await asyncio.start_server(
                self.handle_request, host=host, port=port
            )
            logger.info(f"Proxy server listening on {host}:{port}")
        else:
            raise ValueError(
                "Either 'port' or 'socket' must be specified in listen config"
            )

        async with server:
            await server.serve_forever()
