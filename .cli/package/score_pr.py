import re
import math
from datetime import datetime
from .utils import iter_markdown_files, process_file, is_task

TODAY = datetime.now().date()

field_name = "priority"  # <-- configurable field name


def normalize_score(score):
    if not score or not str(score).strip():
        return 0.0
    try:
        val = float(str(score).strip())
        return max(0.0, min(1.0, (val - 1) / 4))
    except:
        return 0.0


def parse_due_date(due_str):
    if not due_str or not str(due_str).strip():
        return float("inf")
    due_str = str(due_str).strip()
    for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y", "%Y.%m.%d"]:
        try:
            due_date = datetime.strptime(due_str, fmt).date()
            return max(0.0, (due_date - TODAY).days)
        except:
            continue
    return float("inf")


def compute_priority(load, force, necessity, value, due):
    params = {
        "alpha": 1.5,
        "beta": 2.0,
        "gamma": 2.5,
        "delta": 1.5,
        "w_L": 0.4,
        "w_F": 0.8,
        "k": 5.0,
        "theta": 0.75,
        "max_days": 60,
    }
    L = normalize_score(load)
    F = normalize_score(force)
    N = normalize_score(necessity)
    V = normalize_score(value)
    D = parse_due_date(due)
    if math.isinf(D):
        U = 1.0 * (1 + params["beta"] * N)
    else:
        D = min(D, params["max_days"])
        U = (1 / (D + 1) ** params["alpha"]) * (1 + params["beta"] * N)
    S = N ** params["gamma"] + (1 - N) * (V ** params["delta"])
    E = math.exp(-(params["w_L"] * L + params["w_F"] * F))
    priority = U * S * E
    G = 1 / (1 + math.exp(params["k"] * (F - params["theta"])))
    return round(priority * G * 100, 2)


field_pattern = re.compile(r"\[(\w+)::\s*(.*?)\]")


def extract_fields(line):
    fields = dict(field_pattern.findall(line))
    return {
        "load": fields.get("load", ""),
        "force": fields.get("force", ""),
        "necessity": fields.get("necessity", ""),
        "value": fields.get("value", ""),
        "due": fields.get("due", ""),
    }


def update_priority(line, pr):
    # Remove existing field_name field if present
    line = re.sub(rf"\[{re.escape(field_name)}::.*?\]", "", line).strip()
    return f"{line} [{field_name}:: {pr}]\n"


def process_line(line, reset):
    if not is_task(line):
        return line

    if "#task" not in line:
        return line
    # Skip if field already exists and reset is False
    if not reset and re.search(rf"\[{re.escape(field_name)}::", line):
        return line
    fields = extract_fields(line)
    pr = compute_priority(
        fields["load"],
        fields["force"],
        fields["necessity"],
        fields["value"],
        fields["due"],
    )
    return update_priority(line, pr)


def run(reset=False):
    for f in iter_markdown_files():
        process_file(f, lambda line: process_line(line, reset))
