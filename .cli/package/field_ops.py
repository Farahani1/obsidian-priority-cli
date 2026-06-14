import re
from .utils import iter_markdown_files, process_file, is_task


def rename_field(old, new):
    pattern = re.compile(rf"\[{old}::")

    def transform(line):
        if is_task(line):
            return pattern.sub(f"[{new}::", line)
        return line

    for f in iter_markdown_files():
        process_file(f, transform)


def add_field(name, default):
    pattern = re.compile(rf"\[{name}::")

    def transform(line):
        if is_task(line) and not pattern.search(line):
            value = default
            return line.rstrip() + f" [{name}:: {value}]\n"
        return line

    for f in iter_markdown_files():
        process_file(f, transform)


def update_field(name, old_value, new_value):
    pattern = re.compile(rf"\[{name}::\s*{re.escape(old_value)}\]")

    def transform(line):
        if is_task(line):
            return pattern.sub(f"[{name}:: {new_value}]", line)
        return line

    for f in iter_markdown_files():
        process_file(f, transform)