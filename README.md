
# Obsidian-Based Task Management System

### (Templater + Dataview Architecture)

---

# 1. Overview

This system is a **local-first, highly flexible task management environment** built on top of Obsidian using two core components:

- Templater → structured task creation
    
- Dataview → dynamic querying, filtering, and prioritization
    

The goal of this system is to:

- Minimize cognitive load during task capture
    
- Maximize clarity during task review
    
- Preserve context by embedding tasks inside knowledge notes
    
- Enable powerful, customizable views without relying on external services
    

This design avoids rigid task management paradigms and instead provides a **modular and extensible framework** that adapts to the user’s thinking style.

---

# 2. Core Design Philosophy

## 2.1 Task as Embedded Knowledge

Tasks are not stored in a centralized list. Instead, they are:

- Embedded directly inside notes
    
- Placed within meaningful folders
    
- Connected to projects, ideas, and context
    

This ensures that:

> Tasks are always understood within their original context.

---

## 2.2 Folder Structure as Implicit Metadata

The system leverages Obsidian’s folder hierarchy as a **semantic layer**.

Example:

- `/Projects/ML/` → machine learning tasks
    
- `/Engineering/PLC/` → automation tasks
    

Using Dataview:

- `file.folder` becomes a **taxonomy signal**
    
- No need to duplicate `project::` metadata
    

---

## 2.3 Separation of Concerns

|Layer|Responsibility|
|---|---|
|Notes|Store tasks|
|Templater|Create structured tasks|
|Dataview|Filter, compute, display|
|Dashboard|Decision-making interface|

---

# 3. System Capabilities

## 3.1 Flexible Metadata

Each task can include structured fields:

- stage
    
- priority-related fields (force, load, value, necessity)
    
- type, place, tags
    
- dependencies (`waits-on`)
    

Important:

> All fields are optional (except title)

This allows two modes:

### Simple Mode:

```markdown
- [ ] Buy groceries #task [priority:: 0.0]
```

### Advanced Mode:

```markdown
- [ ] Optimize model #task [priority:: 0.0]
  stage:: staged
  force:: 3
  load:: 2
```

---

## 3.2 Fast Task Creation

Using Templater + hotkey:

- Press shortcut (e.g. `Ctrl + T`)
    
- Fill prompts
    
- Task is inserted instantly
    

This reduces friction and ensures consistency.

---

## 3.3 Distinguishing Real Tasks

All structured tasks include:

```markdown
#task [priority:: 0.0]
```

This prevents interference with generic checkboxes:

```markdown
- [ ] random note ❌ ignored 
- [ ] real task #task ✅ included [priority:: 0.0]
```

---

## 3.4 Powerful Filtering & Views

Dataview enables:

- Filtering by any field
    
- Sorting by computed values
    
- Grouping by folder or status
    
- Creating multiple specialized dashboards
    

---

## 3.5 Dynamic Priority Scoring

Tasks are not statically prioritized.

Instead, priority is computed dynamically:

```text
score = (force + necessity + value) / load
```

This allows:

- adaptive prioritization
    
- no manual recalculation
    
- real-time updates
    

---

# 4. Task Template

## Full Task Template (Templater)

```markdown
- [ ] <% tp.system.prompt("Task title") %> #task [priority:: 0.0]
  created:: <% tp.date.now("YYYY-MM-DD") %>
  due:: <% tp.system.prompt("Due date (optional)") %>
  stage:: <% tp.system.suggester(["perhaps","todo","prioritized","staged","hold","canceled","done"], ["perhaps","todo","prioritized","staged","hold","canceled","done"]) %>
  force:: <% tp.system.suggester(["1","2","3","4"], ["1","2","3","4"]) %>
  load:: <% tp.system.suggester(["1","2","3","4"], ["1","2","3","4"]) %>
  necessity:: <% tp.system.suggester(["1","2","3","4"], ["1","2","3","4"]) %>
  value:: <% tp.system.suggester(["1","2","3","4"], ["1","2","3","4"]) %>
  type:: <% tp.system.prompt("Type (optional)") %>
  place:: <% tp.system.prompt("Place (optional)") %>
  tags:: <% tp.system.prompt("Tags (optional)") %>
  waits-on:: <% tp.system.prompt("Dependency (optional)") %>
```

---

# 5. Example Dataview Dashboards

## 5.1 All Tasks with Context

```dataview
table 
  text as "Task",
  file.link as "Source",
  file.folder as "Area",
  stage
where contains(text, "#task") and !completed [priority:: 0.0]
```

---

## 5.2 High Priority Tasks (Score-Based)

```dataview
table 
  text,
  round(
    (default(force,0) + default(necessity,0) + default(value,0)) 
    / default(load,1),
    2
  ) as Score
where contains(text, "#task") and !completed [priority:: 0.0]
sort Score desc
```

---

## 5.3 Tasks by Stage

```dataview
table text, stage
where contains(text, "#task") and !completed [priority:: 0.0]
group by stage
```

---

## 5.4 Tasks in Specific Directory

```dataview
task
from "Projects"
where contains(text, "#task") and !completed [priority:: 0.0]
```

---

## 5.5 Tasks Waiting on Dependencies

```dataview
table text, waits-on
where contains(text, "#task") and waits-on [priority:: 0.0]
```

---

# 6. Workflow

## Daily Workflow

1. Open dashboard
    
2. Review tasks (filtered views)
    
3. Select tasks for today
    
4. Execute tasks via source notes
    

---

## Task Creation Flow

1. Press template hotkey
    
2. Fill fields (optional)
    
3. Task inserted in context
    

---

## Review Flow

- Use dashboards for:
    
    - prioritization
        
    - filtering
        
    - decision making
        

---

# 7. Flexibility

This system supports multiple usage styles:

|User Type|Behavior|
|---|---|
|Minimalist|Only uses `- [ ] #task`| [priority:: 0.0]
|Structured|Uses selected fields|
|Advanced|Uses full metadata + scoring|

---

# 8. Strengths of the System

- Fully offline
    
- No dependency on external services
    
- Highly customizable
    
- Scales with complexity
    
- Integrates knowledge + execution
    
- Reduces cognitive overload
    

---

# 9. Setup Guide (Step-by-Step)

## Step 1 — Install Obsidian

- Create a vault
    

---

## Step 2 — Enable Core Plugins

- Templates
    

---

## Step 3 — Install Community Plugins

- Dataview
    
- Templater
    

---

## Step 4 — Configure Templater

- Set template folder: `/tasks/templates/`
    
- Create `full_task.md`
    

---

## Step 5 — Assign Hotkey

- Assign shortcut to “Insert template”
    

---

## Step 6 — Create Dashboard

Create `/tasks/dashboard.md` and add Dataview queries

---

## Step 7 — Start Using

- Add tasks inside notes
    
- Use `#task` tag [priority:: 0.0]
    
- Review via dashboard
    

---

# Final Note

This system is not just a task manager.

It is a **cognitive interface** that transforms:

- scattered thoughts → structured execution
    
- context → action
    
- complexity → clarity
    

---

## update_desicsions.py
Update task priorities in Obsidian vault

positional arguments:
  vault_path            Path to your Obsidian vault

options:
  -h, --help            show this help message and exit
  --reset               Recompute priorities for ALL tasks (overwrite existing)