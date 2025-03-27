import io
import sys
from unittest.mock import MagicMock, patch

import pytest

from auth_proxy.validate import main, validate_path


def test_validate_path_authenticated(basic_config):
    """Test validation of an authenticated path."""
    # Patch the print function to capture output
    with patch("builtins.print") as mock_print:
        validate_path(basic_config, "/api/resource")

    # Check that the expected output was printed
    mock_print.assert_any_call("Path: /api/resource")
    mock_print.assert_any_call("Matching rule #1: /api/")
    mock_print.assert_any_call("Authentication required: True")
    mock_print.assert_any_call("Authentication plugins: mock")


def test_validate_path_unauthenticated(basic_config):
    """Test validation of an unauthenticated path."""
    # Patch the print function to capture output
    with patch("builtins.print") as mock_print:
        validate_path(basic_config, "/public/index.html")

    # Check that the expected output was printed
    mock_print.assert_any_call("Path: /public/index.html")
    mock_print.assert_any_call("Matching rule #2: /public/")
    mock_print.assert_any_call("Authentication required: False")


def test_validate_path_default(basic_config):
    """Test validation of a path that uses default behavior."""
    # Patch the print function to capture output
    with patch("builtins.print") as mock_print:
        validate_path(basic_config, "/other/path")

    # Check that the expected output was printed
    mock_print.assert_any_call("Path: /other/path")
    mock_print.assert_any_call("No matching rule, using default behavior")
    mock_print.assert_any_call("Authentication required: True")
    mock_print.assert_any_call("Authentication plugins: mock")


def test_validate_path_regex(regex_config):
    """Test validation of a path with regex rules."""
    # Patch the print function to capture output
    with patch("builtins.print") as mock_print:
        validate_path(regex_config, "/api/v1/admin/users")

    # Check that the expected output was printed
    mock_print.assert_any_call("Path: /api/v1/admin/users")
    mock_print.assert_any_call("Authentication required: True")
    mock_print.assert_any_call("Authentication plugins: mock-admin")


def test_main_function():
    """Test the main function of the validation tool."""
    # Mock command line arguments
    test_args = ["auth-proxy-validate", "-c", "config.yaml", "/api/resource"]

    # Mock config file
    mock_config = {
        "paths": [{"path": "/api/", "authenticate": True, "plugins": ["mock"]}],
        "auth": {
            "default_plugins": ["mock"],
            "default_mode": "any",
            "default_behavior": "authenticated",
        },
    }

    with patch("sys.argv", test_args), patch("builtins.open", MagicMock()), patch(
        "yaml.safe_load", return_value=mock_config
    ), patch("auth_proxy.validate.validate_path") as mock_validate:

        main()

        # Check that validate_path was called with the right arguments
        mock_validate.assert_called_once_with(mock_config, "/api/resource")


def test_main_function_file_not_found():
    """Test the main function with a non-existent config file."""
    # Mock command line arguments
    test_args = ["auth-proxy-validate", "-c", "nonexistent.yaml", "/api/resource"]

    with patch("sys.argv", test_args), patch(
        "builtins.open", side_effect=FileNotFoundError
    ), patch("sys.exit") as mock_exit, patch("logging.error") as mock_error:

        main()

        # Check that the error was logged and the program exited
        mock_error.assert_called_once()
        mock_exit.assert_called_once_with(1)
