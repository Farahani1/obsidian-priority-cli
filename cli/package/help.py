import io
import sys

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def show_help():
    help_text = """
TASKS CLI — Local Task Refactoring Engine
========================================

OVERVIEW -DESIGN PHILOSOPHY
---------------------------
This tool do batch operations on your (structured inline-field) Obsidian tasks:
    - [ ] Task title #task [key:: value] [key:: value]

Processing Markdown as structured data, hopefully gives you:
    - consistency > flexibility
    - explicit schema > implicit assumptions
    
If things break:
    → run doctor
    → then normalize



COMMANDS
--------------

# --- TAG OPERATIONS COMMANDS ---
task tag mv <old-tag> <new-tag>
    Rename a tag across all tasks

task tag rm <tag>
    Remove a tag from all tasks


# --- FIELD OPERATIONS COMMANDS ---
task field mv <old-name> <new-name>
    Rename a field key

task field add <name> [default-value]
    Add field to tasks that don't have it

task field update <name> <old> <new>
    Replace a field value globally


# --- SYSTEM COMMANDS ---
task normalize
    Enforce canonical format:
        - consistent spacing
        - ordered fields
        - remove duplicates

task doctor
    Detect problems:
        - missing required fields
        - duplicate fields
        - unknown fields
        - malformed syntax


# --- COMPUTATION COMMANDS ---
task packages score_pr [--reset]
    Compute priority score using:
        load, force, necessity, value, due

    --reset → recompute all tasks
    default → only fill missing priorities


CONFIGURATION (IMPORTANT)
-------------------------

#  --- TASK FORMAT --- 
Canonical structure:
    - [ ] Title #task #tag1 #tag2
      [id:: ...] [title:: ...] [stage:: ...] [priority:: ...]
Rules:
    - Use EXACT syntax: [key:: value]
    - No duplicate fields
    - No unknown fields (unless allowed in config)
    - Tags must include #task to be processed

    
# --- CONFIG FILE ---
File location: ./cli/config.json
Key responsibilities:
    - define vault path
    - define schema (allowed/required fields)
    - control auto behaviors (doctor, normalize)
    - enable/disable customaizable computational scoring modules

========================================
"""
    print(help_text)