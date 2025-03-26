"""Version management tool for Python projects."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from dsbase.log import LocalLogger

if TYPE_CHECKING:
    from logging import Logger


class MonorepoHelper:
    """Helper for monorepo detection and package management."""

    logger: Logger = LocalLogger().get_logger()

    @staticmethod
    def is_monorepo(directory: Path) -> bool:
        """Determine if a directory is part of a monorepo."""
        # Check for packages directory with multiple packages
        packages_dir = directory / "packages"
        if packages_dir.exists() and packages_dir.is_dir():
            # Count subdirectories that contain pyproject.toml
            package_count = sum(
                1 for d in packages_dir.iterdir() if d.is_dir() and (d / "pyproject.toml").exists()
            )
            if package_count > 1:
                return True

        # Check for monorepo configuration in pyproject.toml
        pyproject_path = directory / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomllib

                data = tomllib.loads(pyproject_path.read_text())
                if "tool" in data and "monorepo" in data["tool"]:
                    return True
            except (tomllib.TOMLDecodeError, KeyError):
                pass

        return False

    @classmethod
    def find_monorepo_root(cls, start_dir: Path) -> Path | None:
        """Find the root of the monorepo starting from a given directory."""
        current = start_dir
        # Limit the search to avoid going too far up
        for _ in range(5):
            if cls.is_monorepo(current):
                return current

            parent = current.parent
            if parent == current:  # Reached filesystem root
                break
            current = parent

        return None

    @classmethod
    def auto_detect_package(cls) -> tuple[str, Path]:
        """Try to determine the package from the current directory."""
        current_dir = Path.cwd()

        # Check if we're in a standard repository with pyproject.toml
        if (current_dir / "pyproject.toml").exists():
            # Check if this is a monorepo root
            if cls.is_monorepo(current_dir):
                # We're in a monorepo root, but check if the monorepo is a package
                try:
                    import tomllib

                    pyproject_data = tomllib.loads((current_dir / "pyproject.toml").read_text())
                    if "project" in pyproject_data:
                        # The monorepo root is also a package
                        package_name = pyproject_data["project"].get("name")
                        if not package_name:
                            # Try to get name from directory
                            package_name = current_dir.name
                        package_path = current_dir
                        return package_name, package_path
                except (tomllib.TOMLDecodeError, KeyError):
                    pass

                # If we get here, the monorepo root is not a package itself
                cls.logger.error("You're in a monorepo root. Please use --package to specify.")
                sys.exit(1)

            # We're in a standard repository
            package_name = current_dir.name  # Use directory name as package name
            package_path = current_dir  # Use current directory as package path
            return package_name, package_path

        cls.logger.error("Could not auto-detect package. Please use --package to specify.")
        sys.exit(1)

    @classmethod
    def find_package_in_monorepo(cls, package_name: str) -> tuple[str, Path]:
        """Find a package by name from the monorepo root."""
        current_dir = Path.cwd()

        # Try to find monorepo root
        monorepo_root = cls.find_monorepo_root(current_dir)
        if not monorepo_root:
            print("Error: Could not find monorepo root. Please run from within a monorepo.")
            sys.exit(1)

        # Look for the package in common locations
        possible_paths = [
            monorepo_root / "packages" / package_name,  # packages/name
            monorepo_root / "src" / package_name,  # src/name
            monorepo_root / package_name,  # direct subdirectory
        ]

        for path in possible_paths:
            if path.exists() and (path / "pyproject.toml").exists():
                return package_name, path

        print(f"Error: Could not find package '{package_name}' in the monorepo.")
        print(f"Searched in: {', '.join(str(p) for p in possible_paths)}")
        sys.exit(1)

    @classmethod
    def detect_package(cls, package_arg: str | None = None) -> tuple[str, Path]:
        """Detect package and relevant paths."""
        # Auto-detect package if not provided
        if package_arg is None:
            package_name, package_path = cls.auto_detect_package()
        else:
            # Try to find the package in a monorepo first
            current_dir = Path.cwd()
            monorepo_root = cls.find_monorepo_root(current_dir)

            if monorepo_root:
                package_name, package_path = cls.find_package_in_monorepo(package_arg)
            # Not in a monorepo, treat as standard repository
            elif (current_dir / "pyproject.toml").exists():
                package_name = package_arg
                package_path = current_dir
            else:
                print("Error: Not in a repository with pyproject.toml")
                sys.exit(1)

        # Verify package exists
        if not package_path.exists():
            print(f"Error: Package directory '{package_path}' not found")
            sys.exit(1)

        return package_name, package_path
