# CLI Guide

This document explains how the Task Priority command-line tool is organized and how commands flow through the system.

## Directory model

The tool is intended to live inside the task-focused directory of an Obsidian vault, not necessarily at the root of the entire vault.

Example layout:

```text
ObsidianVault/
  notes/
  references/
  tasks/
    .cli/
      task.py
      config.json
      package/
    project-task-note.md
    another-task-note.md
```

In this model, the task directory is the workspace that the CLI scans and modifies. This keeps unrelated notes out of batch task operations while still allowing everything to remain in a single Obsidian vault.

## Running the CLI

The project is designed to use Python's built-in libraries only. A virtual environment is not required.

From the task directory, commands can be run as:

```bash
python3 .cli/task.py <command> [arguments]
```

On Windows, the equivalent may be:

```powershell
python .cli/task.py <command> [arguments]
```

## Configuration

The CLI reads `.cli/config.json` through `package/config.py`.

The most important path settings are:

```json
{
  "vault_path": "..",
  "log_dir": "."
}
```

When `.cli` is located inside the task directory, `vault_path` should resolve to the parent directory of `.cli`, meaning the task workspace itself.

Path resolution should be centralized in `config.py` so other modules do not need to know whether paths are relative or absolute.

## Command flow

The entry point is `.cli/task.py`.

A typical mutating command follows this pattern:

1. Load configuration.
2. Run preflight checks.
3. Optionally run doctor validation.
4. Optionally normalize task formatting.
5. Create a version-control snapshot before mutation.
6. Dispatch the requested operation.
7. Modify matching Markdown task lines.

## Commands

```bash
python3 .cli/task.py tag mv <old-tag> <new-tag>
python3 .cli/task.py tag rm <tag>
python3 .cli/task.py field mv <old-name> <new-name>
python3 .cli/task.py field add <name> [default-value]
python3 .cli/task.py field update <name> <old-value> <new-value>
python3 .cli/task.py normalize
python3 .cli/task.py packages score_pr [--reset]
```

## Task and field format

A task is an Obsidian checkbox line with structured inline fields:

```markdown
- [ ] Example task #task [id:: example-001] [stage:: todo] [priority:: 0.0]
```

Fields use this syntax:

```markdown
[key:: value]
```

The doctor module checks for missing required fields, duplicate fields, unknown fields, and malformed field syntax.

## Priority scoring

The priority scorer reads fields such as `load`, `force`, `necessity`, `value`, and `due`.

Without `--reset`, existing priority values are preserved. With `--reset`, priorities are recomputed.

## Version-control behavior

The history module uses Git to snapshot the task workspace before mutating operations.

The intended behavior is:

1. Initialize a Git repository in the configured task workspace if one does not exist.
2. Commit the current state before a mutating command.
3. Run the mutation.
4. Allow undo to restore the previous snapshot.

Because Git searches parent directories for `.git`, the implementation should verify that Git is operating inside the configured task workspace, not accidentally using a parent repository.

Useful debug commands:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git status
git log --oneline
```

## Privacy expectations

The CLI is local-first and works on local Markdown files. It does not require an external task-management service for core operations.
