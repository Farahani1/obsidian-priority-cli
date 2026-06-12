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
    # Ensure tag has the '#' prefix
    if not tag.startswith('#'):
        tag = '#' + tag
    
    # Match optional whitespace + the exact tag
    pattern = re.compile(rf"\s*{re.escape(tag)}")
    
    def transform(line):
        if is_task(line):
            # Remove the tag and any whitespace immediately before it
            line = pattern.sub("", line)
            # Clean up multiple spaces (optional but nice)
            line = re.sub(r'  +', ' ', line).strip()
            return line
        return line
    
    for f in iter_markdown_files():
        process_file(f, transform)