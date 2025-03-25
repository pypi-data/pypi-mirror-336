import importlib
import os
import sys
from collections.abc import Generator
from pathlib import Path
from types import ModuleType


def list_modules(root_package_path: Path) -> Generator[ModuleType]:
    for module_path in list_module_paths(root_package_path):
        yield import_module(root_package_path, module_path)


def list_module_paths(root_package_path: Path) -> Generator[Path]:
    for file_path in list_file_paths(root_package_path):
        if _is_module(file_path):
            yield file_path


def list_file_paths(root_package_path: Path) -> Generator[Path]:
    for directory, _, file_names in os.walk(root_package_path):
        directory_path = Path(directory)

        for file_name in file_names:
            yield directory_path / Path(file_name)


def _is_module(path: Path) -> bool:
    file_name = path.name

    return file_name.endswith(".py")


def import_module(root_package_path: Path, module_path: Path) -> ModuleType:
    if not _root_package_in_path(root_package_path):
        _add_root_package_to_path(root_package_path)

    return _import_module(root_package_path, module_path)


def _import_module(root_package_path: Path, module_path: Path) -> ModuleType:
    module_name = get_module_name(module_path, root_package_path)

    return importlib.import_module(module_name)


def _root_package_in_path(root_package_path: Path) -> bool:
    return _get_package_parent_string(root_package_path) in sys.path


def _get_package_parent_string(package_path: Path) -> str:
    parent_path = package_path.parent

    return str(parent_path)


def _add_root_package_to_path(root_package_path: Path):
    parent_path = root_package_path.parent
    parent_path_string = str(parent_path)

    _add_to_path(parent_path_string)


def _add_to_path(path_string: str) -> None:
    sys.path.insert(0, path_string)


def get_module_name(module_path: Path, package_root_path: Path):
    relative = module_path.relative_to(package_root_path.parent)

    return ".".join(relative.with_suffix("").parts)
