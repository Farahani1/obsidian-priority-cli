
```dataview
TABLE 
  t.id AS "ID",
  t.title AS "Task",
  t.stage AS "Stage",
  join(filter(t.tags, (x) => x != "#task"), " ") AS "Tags",
  t.force AS "F",
  t.load AS "L",
  t.necessity AS "N",
  t.value AS "V",
  t.priority AS "Priority",
  t.due AS "Due"
FROM ""
FLATTEN file.tasks AS t
WHERE !t.completed AND contains(t.tags, "office")
SORT t.priority DESC
```


