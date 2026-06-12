# Obsidian Dataview — Task Database Query Guide

A practical reference for querying an inline-metadata task system in [Obsidian](https://obsidian.md/) using the [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) plugin.

This guide assumes your tasks are stored as Obsidian checklist items with inline fields, following a structure similar to:

```
- [ ] Buy groceries #house #errands [id:: a1b2] [priority:: 0.45] [load:: 1] [value:: 3] [due:: 2024-06-15] [status:: todo]
```

---

## Table of Contents

1. [Task Field Reference](#task-field-reference) [priority:: 0.0]
2. [Master Query Template](#master-query-template)
3. [Filtering](#filtering)
4. [Sorting](#sorting)
5. [Column Control](#column-control)
6. [Ready-to-Use Views](#ready-to-use-views)
7. [Common Mistakes](#common-mistakes)
8. [Hard Rules](#hard-rules)

---

## Task Field Reference

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique task identifier |
| `title` | string | Task name / description |
| `stage` | string | Workflow stage (`idea`, `todo`, `doing`, `done`) |
| `tags` | list | Context tags (e.g. `#home`, `#work`) |
| `force` | number | Motivational force (e.g. 1–5) |
| `load` | number | Effort required (e.g. 1–5) |
| `necessity` | number | How necessary this is (e.g. 1–5) |
| `value` | number | Expected outcome value (e.g. 1–5) |
| `priority` | number | Computed priority score (e.g. 0.0–1.0) |
| `due` | date | Due date |

> **Note:** `priority` can be a manually set value or a computed formula combining `force`, `load`, `necessity`, and `value`.

---

## Master Query Template

Use this as your base and modify from here:

```dataview
TABLE 
  t.id AS "ID",
  t.title AS "Task",
  t.stage AS "Stage",
join(filter(t.tags, (x) => x != "#task"), " ") AS "Tags", [priority:: 0.0]
  t.force AS "F",
  t.load AS "L",
  t.necessity AS "N",
  t.value AS "V",
  t.priority AS "Priority",
  t.due AS "Due"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed
SORT t.priority DESC
```

---

## Filtering

### By tag

Show only tasks that carry a specific tag:

```dataview
WHERE contains(t.tags, "#home")
```

### By multiple tags (AND)

Tasks that carry **all** specified tags:

```dataview
WHERE contains(t.tags, "#home") AND contains(t.tags, "#office")
```

### By multiple tags (OR)

Tasks that carry **any** of the specified tags:

```dataview
WHERE contains(t.tags, "#home") OR contains(t.tags, "#office")
```

### By stage

```dataview
WHERE t.stage = "todo"
```

Multiple stages:

```dataview
WHERE t.stage = "todo" OR t.stage = "idea"
```
### By Scope(location)

Dataview gives you:
```
file.path
file.folder
file.name
```

For including subdirectories:
```
WHERE contains(file.path, "Projects/Home")
```

For Exact folder only (no subfolders):
```
WHERE file.folder = "Projects/Home"
```


### By priority threshold

```dataview
WHERE t.priority >= 0.3
```

### By due date (tasks that have a due date set)

```dataview
WHERE t.due
```

### Combining filters

```dataview
WHERE 
  contains(t.tags, "#home") AND 
  t.stage = "todo" AND 
  t.priority > 0.2
```

### Debugging a single task by ID

```dataview
WHERE t.id = "4l1a"
```

### Completed vs. unfinished

Only unfinished tasks:

```dataview
WHERE !t.completed
```

Only completed tasks:

```dataview
WHERE t.completed
```

---

## Sorting

### By priority (highest first)

```dataview
SORT t.priority DESC
```

### By due date (most urgent first)

```dataview
SORT t.due ASC
```

### Multi-level sort

Priority first, then urgency as a tiebreaker:

```dataview
SORT t.priority DESC, t.due ASC
```

---

## Column Control

### Minimal view

```dataview
TABLE 
  t.title AS "Task",
  t.stage AS "Stage",
  t.priority AS "Priority"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed
SORT t.priority DESC
```

### Adding extra columns

Any inline field can be added as a column:

```dataview
TABLE 
  t.title AS "Task",
  t.created AS "Created",
  t.id AS "ID"
```

### Limit results

Show only the top N rows:

```dataview
LIMIT 10
```

---

## Ready-to-Use Views

### 1. What should I work on now?

Top 10 open tasks by priority:

```dataview
TABLE t.title AS "Task", t.priority AS "Priority", t.stage AS "Stage"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed
SORT t.priority DESC
LIMIT 10
```

---

### 2. Tasks by context tag

All open home tasks:

```dataview
TABLE t.title AS "Task", t.priority AS "Priority"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed AND contains(t.tags, "#home")
SORT t.priority DESC
```

---

### 3. Urgent and important

Tasks with a due date and meaningful priority:

```dataview
TABLE t.title AS "Task", t.due AS "Due", t.priority AS "Priority"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed AND t.due AND t.priority > 0.2
SORT t.due ASC
```

---

### 4. Low effort, high value (quick wins)

```dataview
TABLE t.title AS "Task", t.value AS "Value", t.load AS "Load"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed AND t.value >= 3 AND t.load <= 2
SORT t.value DESC
```

---

## Common Mistakes

### Tags with commas — incorrect format

```
#home, #work, #errands
```

Dataview cannot parse comma-separated tags. Use space-separated tags instead:

```
#home #work #errands
```

### Forgetting to flatten

Without `FLATTEN file.tasks AS t`, Dataview operates on files rather than individual task items and none of the `t.*` field references will work.

### Multi-line tasks

Each task must be a single line. Inline fields on a continuation line will not be picked up by Dataview.

---

## Hard Rules

1. **Always include the flatten clause:**
   ```dataview
   FLATTEN file.tasks AS t
   ```

2. **Always prefix field references with `t.`** — e.g. `t.priority`, not just `priority`.

3. **One task = one line** — do not break a task across multiple lines.

4. **Tags use spaces, not commas:**
   ```
   ✅  #tag1 #tag2 #tag3
   ❌  #tag1, #tag2, #tag3
   ```

---

## Further Reading

- [Dataview documentation](https://blacksmithgu.github.io/obsidian-dataview/) 
- [Dataview inline fields reference](https://blacksmithgu.github.io/obsidian-dataview/data-annotation/) 
- [Obsidian community plugins](https://obsidian.md/plugins) 
