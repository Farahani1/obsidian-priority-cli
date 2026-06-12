import re
from .utils import iter_markdown_files, is_task
from .config import load_config

field_pattern = re.compile(r'\[(\w+)::\s*(.*?)\]')


def analyze_line(line, config):
    issues = []

    fields = field_pattern.findall(line)
    keys = [k for k, _ in fields]

    # Duplicate fields
    if len(keys) != len(set(keys)):
        issues.append("duplicate_fields")

    # Required fields
    for req in config["fields"]["required"]:
        if req not in keys:
            issues.append(f"missing:{req}")

    # Unknown fields
    allowed = set(config["fields"]["allowed"])
    for k in keys:
        if k not in allowed:
            issues.append(f"unknown:{k}")

    # Malformed syntax
    if "[" in line and not field_pattern.search(line):
        issues.append("malformed_field")

    return issues


def run():
    config = load_config()
    total = 0
    problems = 0

    for f in iter_markdown_files():
        with open(f, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                if is_task(line):
                    total += 1
                    issues = analyze_line(line, config)

                    if issues:
                        problems += 1
                        print(f"{f}:{i+1}")
                        print(f"  → {', '.join(issues)}")
                        print(f"  → {line.strip()}\n")

    print("=" * 60)
    print(f"Checked {total} tasks | Problems: {problems}")
    print("=" * 60)

    return problems