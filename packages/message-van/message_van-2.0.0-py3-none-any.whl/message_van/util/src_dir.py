from pathlib import Path


def get_src_dir(start_path: Path) -> Path:
    start_path = start_path.resolve()

    for parent in [start_path, *start_path.parents]:
        if _is_src_dir(parent):
            return parent


def _is_src_dir(path: Path) -> bool:
    return path.name == "src" or path.parent.name == "site-packages"
