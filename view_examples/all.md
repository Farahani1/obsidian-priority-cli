
# Idea
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
WHERE !t.completed AND t.stage = "O"
SORT t.priority DESC
```


# Todo
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
WHERE !t.completed AND t.stage = "|O|"
SORT t.priority DESC
```



# Priority
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
WHERE !t.completed AND t.stage = "@"
SORT t.priority DESC
```


# In-Session
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
WHERE !t.completed AND t.stage = "&"
SORT t.priority DESC
```



