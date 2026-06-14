import re
from .utils import iter_markdown_files, process_file, is_task
from .config import load_config


FIELD_ORDER = [
    "id", "title", "stage", "priority",
    "force", "load", "necessity", "value", "due"
]

field_pattern = re.compile(r'\[(\w+)::\s*(.*?)\]')


def normalize_line(line: str) -> str:
    if not is_task(line):
        return line

    # Extract fields
    fields = dict(field_pattern.findall(line))

    # Remove all fields from line
    line_clean = field_pattern.sub('', line)

    # Normalize spacing
    line_clean = re.sub(r'\s+', ' ', line_clean).strip()

    # Rebuild fields in canonical order
    ordered_fields = []
    for key in FIELD_ORDER:
        if key in fields:
            ordered_fields.append(f"[{key}:: {fields[key]}]")

    # Add remaining fields (unknown ones)
    for key, val in fields.items():
        if key not in FIELD_ORDER:
            ordered_fields.append(f"[{key}:: {val}]")

    return line_clean + " " + " ".join(ordered_fields) + "\n"

# keep previous code, just modify:

def normalize_all():
    config = load_config()

    if not config["normalize"]["auto_run"]:
        return

    for f in iter_markdown_files():
        process_file(f, normalize_line)