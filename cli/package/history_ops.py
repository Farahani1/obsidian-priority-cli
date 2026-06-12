import subprocess
import json
from pathlib import Path
from datetime import datetime
from .config import load_config

config = load_config()

LOG_DIR = Path(config['log_dir'])
LOG_FILE = LOG_DIR / "log.json"


# -----------------------------
# GIT HELPERS
# -----------------------------

def run_git(args, cwd):
    return subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )


def get_head_commit(vault_path):
    result = run_git(["rev-parse", "HEAD"], vault_path)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


# -----------------------------
# INIT
# -----------------------------

def ensure_repo(vault_path):
    vault = Path(vault_path)
    git_dir = vault / ".git"

    if not git_dir.exists():
        print("[INIT] Initializing git repository...")
        run_git(["init"], vault_path)
        run_git(["add", "."], vault_path)
        run_git(["commit", "-m", "Initial snapshot"], vault_path)

    LOG_DIR.mkdir(exist_ok=True)

    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            json.dump([], f)


# -----------------------------
# LOGGING
# -----------------------------

def append_log(entry):
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# SNAPSHOT BEFORE CHANGE
# -----------------------------

def before_change(command_str):
    config = load_config()
    vault_path = Path(config["vault_path"]).resolve()

    ensure_repo(vault_path)

    # Stage changes
    run_git(["add", "."], vault_path)

    # Commit
    msg = f"task: {command_str}"
    result = run_git(["commit", "-m", msg], vault_path)

    # If nothing to commit → skip
    if "nothing to commit" in result.stdout.lower():
        commit_id = get_head_commit(vault_path)
    else:
        commit_id = get_head_commit(vault_path)

    # Log
    append_log({
        "change_id": commit_id,
        "command": command_str,
        "timestamp": datetime.now().isoformat()
    })

    return commit_id


# -----------------------------
# LOG VIEW
# -----------------------------

def show_log(limit=10):
    if not LOG_FILE.exists():
        print("No history found.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    for entry in reversed(data[-limit:]):
        cid = entry["change_id"][:7]
        print(f"{entry['timestamp']} | {cid} | {entry['command']}")


# -----------------------------
# UNDO
# -----------------------------

def undo(change_id=None):
    config = load_config()
    vault_path = Path(config["vault_path"]).resolve()

    if change_id:
        print(f"[UNDO] Reset to {change_id}")
        run_git(["reset", "--hard", change_id], vault_path)
        return

    print("[UNDO] Reverting last change...")
    run_git(["reset", "--hard", "HEAD~1"], vault_path)

    # Update log
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            data = json.load(f)

        if data:
            data.pop()

        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)