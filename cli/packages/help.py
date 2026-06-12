def show_help():
    help_text = """
TASKS CLI — Local Task Refactoring Engine
========================================

OVERVIEW
--------
This tool performs batch operations on your Obsidian task system.
It assumes tasks follow a structured inline-field format:

    - [ ] Task title #task [key:: value] [key:: value]

The system enforces a canonical format via:
    - doctor     → detect problems
    - normalize  → fix structure

These may run automatically based on config.


BASIC COMMANDS
--------------

# --- TAG OPERATIONS ---
tasks tag mv <old-tag> <new-tag>
    Rename a tag across all tasks

tasks tag rm <tag>
    Remove a tag from all tasks


# --- FIELD OPERATIONS ---
tasks field mv <old-name> <new-name>
    Rename a field key

tasks field add <name> [default-value]
    Add field to tasks that don't have it

tasks field update <name> <old> <new>
    Replace a field value globally


# --- SYSTEM COMMANDS ---
tasks normalize
    Enforce canonical format:
        - consistent spacing
        - ordered fields
        - remove duplicates

tasks doctor
    Detect problems:
        - missing required fields
        - duplicate fields
        - unknown fields
        - malformed syntax


# --- COMPUTATION ---
tasks packages score_pr [--reset]
    Compute priority score using:
        load, force, necessity, value, due

    --reset → recompute all tasks
    default → only fill missing priorities


EXECUTION MODEL
---------------
Before most commands:
    1. doctor runs (validation)
    2. normalize runs (optional, config-controlled)

This ensures system consistency.


TASK FORMAT (IMPORTANT)
----------------------
Canonical structure:

    - [ ] Title #task #tag1 #tag2
      [id:: ...] [title:: ...] [stage:: ...] [priority:: ...]

Rules:
    - Use EXACT syntax: [key:: value]
    - No duplicate fields
    - No unknown fields (unless allowed in config)
    - Tags must include #task to be processed


CONFIGURATION
-------------
Location:
    _task/_config/config.json

Key responsibilities:
    - define vault path
    - define schema (allowed/required fields)
    - control auto behaviors (doctor, normalize)
    - enable/disable scoring modules


COMMON WORKFLOWS
----------------

# Fix system drift
tasks normalize

# Check problems
tasks doctor

# Recompute priorities
tasks packages score_pr --reset

# Rename a field globally
tasks field mv urgency priority


DESIGN PHILOSOPHY
-----------------
This system treats Markdown as structured data.

That means:
    - consistency > flexibility
    - explicit schema > implicit assumptions

If things break:
    → run doctor
    → then normalize


========================================
"""
    print(help_text)