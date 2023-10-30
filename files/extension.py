import sys
import json
import pathlib

if len(sys.argv) == 1:
    json.dump(
        {
            "title": "File Browser",
            "commands": [
                {
                    "name": "ls",
                    "title": "List files",
                    "mode": "page",
                    "params": [
                        {"name": "dir", "type": "string"},
                        {"name": "show-hidden", "type": "boolean"},
                    ],
                }
            ],
        },
        sys.stdout,
        indent=4,
    )
    sys.exit(0)

input = json.loads(sys.argv[1])
if input["command"] == "ls":
    params = input["params"]
    root = pathlib.Path(params.get("dir", "."))
    show_hidden = params.get("show-hidden", False)

    items = []
    for file in root.iterdir():
        if not show_hidden and file.name.startswith("."):
            continue
        item = {
            "title": file.name,
            "subtitle": "📦" if file.is_dir() else "",
            "accessories": [str(file.absolute())],
            "actions": [],
        }
        if file.is_dir():
            item["actions"].append(
                {
                    "title": "Browse",
                    "type": "run",
                    "command": "ls",
                    "params": {
                        "dir": str(file.absolute()),
                    },
                }
            )
        item["actions"].extend(
            [
                {
                    "title": "Open",
                    "key": "o",
                    "type": "open",
                    "target": str(file.absolute()),
                    "exit": True,
                },
                {
                    "title": "Show Hidden Files" if not show_hidden else "Hide Hidden Files",
                    "key": "h",
                    "type": "reload",
                    "params": {
                        "show-hidden": not show_hidden,
                        "dir": str(root.absolute()),
                    },
                },
            ]
        )

        items.append(item)

    json.dump(
        {
            "type": "list",
            "items": items,
        },
        sys.stdout,
    )
