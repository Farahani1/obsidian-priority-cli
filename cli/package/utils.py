import os
from pathlib import Path
from .config import load_config

ROOT_DIR = os.getcwd()


def iter_markdown_files():
    config = load_config()
    root = Path(config["vault_path"]).resolve()

    for f in root.rglob("*.md"):
        yield f


def is_task(line):
    return line.strip().startswith("- [")

def read_file_safe(filepath):
    """Read file with fallback encodings."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.readlines(), "utf-8"
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                return f.readlines(), "latin-1"
        except Exception as e:
            print(f"[SKIP] Cannot read {filepath}: {e}")
            return None, None


def write_file_safe(filepath, lines, encoding):
    """Write back using original encoding."""
    try:
        with open(filepath, "w", encoding=encoding) as f:
            f.writelines(lines)
    except Exception as e:
        print(f"[ERROR] Cannot write {filepath}: {e}")


def process_file(filepath, line_fn):
    lines, encoding = read_file_safe(filepath)

    if lines is None:
        return

    new_lines = [line_fn(line) for line in lines]

    write_file_safe(filepath, new_lines, encoding)