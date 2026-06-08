<%*
const title = await tp.system.prompt("Task title");

const tags = await tp.system.prompt("Tags (space separated)");
const stage = await tp.system.prompt("Stage");

const force = await tp.system.prompt("Force (1-5)");
const load = await tp.system.prompt("Load (1-5)");
const necessity = await tp.system.prompt("Necessity (1-5)");
const value = await tp.system.prompt("Value (1-5)");

// short ID (3–4 chars from timestamp)
const id = Date.now().toString(36).slice(-4);

const tag_str = tags.split(" ").map(t => "#" + t).join(" ");

tR = `- [ ] ${title} #task ${tag_str} [id:: ${id}] [title:: ${title}] [stage:: ${stage}] [force:: ${force}] [load:: ${load}] [necessity:: ${necessity}] [value:: ${value}] [due:: ]`;
%>
