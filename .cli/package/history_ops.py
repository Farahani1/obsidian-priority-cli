import subprocess
import json
from pathlib import Path
from datetime import datetime
from .config import load_config


def cfg():
    return load_config()


def log_file() -> Path:
    return cfg().log_file


def vault_path() -> Path:
    return cfg().vault_path


def run_git(args, cwd=None):
    cwd = cwd or vault_path()

    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Git failed: git {' '.join(args)}\n"
            f"cwd: {cwd}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    return result


def get_head_commit():
    result = run_git(["rev-parse", "HEAD"])
    return result.stdout.strip()


def ensure_repo():
    vault = vault_path()

    if not (vault / ".git").exists():
        print("[INIT] Initializing git repository...")
        run_git(["init"])
        run_git(["add", "."])
        run_git(["commit", "--allow-empty", "-m", "Initial snapshot"])

    lf = log_file()
    lf.parent.mkdir(parents=True, exist_ok=True)

    if not lf.exists():
        lf.write_text("[]", encoding="utf-8")


def append_log(entry):
    lf = log_file()

    if lf.exists():
        data = json.loads(lf.read_text(encoding="utf-8"))
    else:
        data = []

    data.append(entry)
    lf.write_text(json.dumps(data, indent=2), encoding="utf-8")


def before_change(command_str):
    ensure_repo()

    run_git(["add", "."])

    status = run_git(["status", "--porcelain"])

    if status.stdout.strip():
        run_git(["commit", "-m", f"task: {command_str}"])
    else:
        # For your current before-change model, this is optional.
        # I would keep it OFF to avoid noisy history.
        pass

    commit_id = get_head_commit()

    append_log({
        "change_id": commit_id,
        "command": command_str,
        "timestamp": datetime.now().isoformat()
    })

    return commit_id


def undo(change_id=None):
    ensure_repo()

    if change_id:
        print(f"[UNDO] Reset to {change_id}")
        run_git(["reset", "--hard", change_id])
    else:
        print("[UNDO] Reset working tree to last snapshot")
        run_git(["reset", "--hard", "HEAD"])

    run_git(["clean", "-fd"])

    lf = log_file()

    if lf.exists():
        data = json.loads(lf.read_text(encoding="utf-8"))

        if change_id:
            data = [x for x in data if x.get("change_id") != change_id]
        elif data:
            data.pop()

        lf.write_text(json.dumps(data, indent=2), encoding="utf-8")