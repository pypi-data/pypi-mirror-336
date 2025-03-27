import argparse
import logging
import re
import sys
from typing import Any, Dict, List, Tuple

import yaml


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=level, format="%(message)s", handlers=[logging.StreamHandler()]
    )


def compile_regex_patterns(paths: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Compile regex patterns in path rules."""
    compiled_paths = []
    for path_rule in paths:
        if path_rule.get("regex", False):
            try:
                pattern = re.compile(path_rule["path"])
                compiled_paths.append({**path_rule, "pattern": pattern})
            except re.error as e:
                logging.error(f"Invalid regex pattern '{path_rule['path']}': {e}")
                sys.exit(1)
        else:
            compiled_paths.append(path_rule)
    return compiled_paths


def find_matching_rule(
    path: str, paths: List[Dict[str, Any]], auth_config: Dict[str, Any]
) -> Tuple[int, Dict[str, Any]]:
    """Find the matching rule for a given path."""
    for i, path_rule in enumerate(paths):
        if "pattern" in path_rule:  # Regex pattern
            if path_rule["pattern"].match(path):
                return i, path_rule
        else:  # Simple prefix matching
            pattern = path_rule.get("path", "")
            if path.startswith(pattern):
                return i, path_rule

    # No matching rule found, use default behavior
    default_behavior = auth_config.get("default_behavior", "authenticated")
    authenticate = default_behavior == "authenticated"
    default_plugins = auth_config.get("default_plugins", [])
    default_mode = auth_config.get("default_mode", "any")

    # Create a default rule
    return -1, {
        "authenticate": authenticate,
        "plugins": default_plugins if authenticate else [],
        "mode": default_mode,
        "path": "<default>",
        "regex": False,
    }


def validate_path(config: Dict[str, Any], path: str) -> None:
    """Validate which rule would match a given path."""
    paths = config.get("paths", [])
    auth_config = config.get("auth", {})

    # Compile regex patterns
    compiled_paths = compile_regex_patterns(paths)

    # Find matching rule
    index, rule = find_matching_rule(path, compiled_paths, auth_config)

    # Display result
    print(f"Path: {path}")
    if index >= 0:
        print(f"Matching rule #{index + 1}: {rule['path']}")
    else:
        print("No matching rule, using default behavior")

    print(f"Authentication required: {rule['authenticate']}")

    if rule["authenticate"]:
        plugins = rule.get("plugins", auth_config.get("default_plugins", []))
        mode = rule.get("mode", auth_config.get("default_mode", "any"))
        print(f"Authentication plugins: {', '.join(plugins) if plugins else 'none'}")
        print(f"Authentication mode: {mode}")

    # Show the full rule for reference
    print("\nFull matching rule:")
    for key, value in rule.items():
        if key != "pattern":  # Skip compiled regex pattern
            print(f"  {key}: {value}")


def main() -> None:
    """Main entry point for validation tool."""
    parser = argparse.ArgumentParser(description="Validate auth-proxy path rules")
    parser.add_argument(
        "-c", "--config", default="config.yaml", help="Path to config file"
    )
    parser.add_argument("path", help="URL path to validate")
    args = parser.parse_args()

    setup_logging()

    try:
        # Load configuration
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        # Validate path
        validate_path(config, args.path)
    except FileNotFoundError:
        logging.error(f"Config file not found: {args.config}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing config file: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
