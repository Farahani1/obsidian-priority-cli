# Task Priority

A local-first CLI for managing and refactoring structured Markdown tasks inside a dedicated task directory in an Obsidian vault.

My motivation for creating this project was that, after an internet blackout in my country, I lost access to the task-management platforms I used to start my day, so I decided to build a local alternative.

## What this project does

Task Priority works directly on Markdown files. It is intended for users who keep many kinds of notes in one Obsidian vault but want task operations to affect only a specific task directory.

The project aims to:

- keep task management local and service-independent
- work with plain Markdown and Obsidian checkbox tasks
- support structured inline fields such as `[priority:: 0.0]`
- batch-edit tags and fields
- normalize task formatting
- compute priority scores from task metadata
- use Git snapshots to make batch edits safer
- rely only on Python's built-in libraries

## Recommended layout

Place `.cli` at the root of the directory dedicated to tasks:

```text
ObsidianVault/
  notes/
  references/
  tasks/
    .cli/
      task.py
      config.json
      package/
    task-note.md
```

In this layout, `tasks/` is the workspace. The CLI should scan and modify that directory, not the whole Obsidian vault.

## Running commands

No virtual environment is required.

From the task directory:

```bash
python3 .cli/task.py help
python3 .cli/task.py tag rm hard
python3 .cli/task.py tag mv old-tag new-tag
python3 .cli/task.py field add stage todo
python3 .cli/task.py normalize
python3 .cli/task.py packages score_pr --reset
```

On Windows, use `python` instead of `python3` if needed.

## Task format

Tasks are Markdown checkbox lines with Obsidian-style inline fields:

```markdown
- [ ] Prepare report #task [id:: report-001] [stage:: todo] [priority:: 0.0]
```

Fields use this syntax:

```markdown
[key:: value]
```

Common fields include `id`, `title`, `stage`, `priority`, `force`, `load`, `necessity`, `value`, and `due`.

## Configuration

Configuration lives in `.cli/config.json`.

For the recommended layout, the path settings should point from `.cli` back to the task workspace:

```json
{
  "vault_path": "..",
  "log_dir": "."
}
```

Path handling should be centralized in `package/config.py` so other modules do not depend on the shell's current working directory.

## Features

### Tag operations

```bash
python3 .cli/task.py tag mv old-tag new-tag
python3 .cli/task.py tag rm hard
```

### Field operations

```bash
python3 .cli/task.py field mv status stage
python3 .cli/task.py field add stage todo
python3 .cli/task.py field update stage todo staged
```

### Normalization

```bash
python3 .cli/task.py normalize
```

### Priority scoring

```bash
python3 .cli/task.py packages score_pr
python3 .cli/task.py packages score_pr --reset
```

The scorer uses fields such as `load`, `force`, `necessity`, `value`, and `due`.

### Version-control snapshots

The history module is intended to use Git snapshots before mutating operations, so batch edits can be inspected and reverted.

Because Git searches upward for parent repositories, verify that Git is operating inside the configured task workspace:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git status
git log --oneline
```

## Documentation

Additional documentation:

- [CLI Guide](docs/cli.md) — command flow, directory model, configuration, task format, and version-control behavior.

## Privacy note

The documentation has been written in generic terms and should not include chat transcripts, private task contents, personal names, or machine-specific paths.

## Status

This project is evolving from an Obsidian task-management concept into a small local CLI for structured Markdown task refactoring.
