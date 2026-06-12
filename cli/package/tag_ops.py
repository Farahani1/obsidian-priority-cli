import re
from .utils import iter_markdown_files, process_file, is_task

def rename_tag(old, new):
    pattern = re.compile(rf"(?<!\w){re.escape(old)}(?!\w)")

    def transform(line):
        if is_task(line):
            return pattern.sub(new, line)
        return line

    for f in iter_markdown_files():
        process_file(f, transform)


def remove_tag(tag):
    pattern = re.compile(rf"\s*{re.escape(tag)}")

    def transform(line):
        if is_task(line):
            return pattern.sub("", line)
        return line

    for f in iter_markdown_files():
        process_file(f, transform)