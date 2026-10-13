import sys
import json

TARGET_PORT = "8080"

for line in sys.stdin:
    try:
        msg = json.loads(line)
    except ValueError:
        continue
    if msg.get("type") != "printf":
        continue

    parts = msg["data"].split("|", 2)
    if len(parts) < 3:
        continue
    pid, comm, raw = parts

    lines = raw.split("\r\n")
    first = lines[0].split(" ")
    if len(first) < 2:
        continue
    method, path = first[0], first[1]

    host = ""
    for l in lines[1:]:
        if l.lower().startswith("host:"):
            host = l.split(":", 1)[1].strip()

    port = host.rsplit(":", 1)[1] if ":" in host else "80"
    if port != TARGET_PORT:
        continue

    event = {"pid": int(pid), "comm": comm, "method": method,
             "path": path, "host": host}
    print(json.dumps(event), flush=True)
