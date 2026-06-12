
# Idea
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
WHERE !t.completed AND t.stage = "O" AND contains(file.path, "task_examples/holiday")
SORT t.priority DESC
```


# Todo


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
WHERE !t.completed AND t.stage = "|O|" AND contains(file.path, "task_examples/holiday")
SORT t.priority DESC
```

