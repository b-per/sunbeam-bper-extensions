import sys
import json

import run_results
import node_details
import running_models

if len(sys.argv) == 1:
    json.dump(
        {
            "title": "dbt",
            "commands": [
                {
                    "name": "run-results",
                    "title": "List models run",
                    "mode": "filter",
                    "params": [
                        {"title": "Include packages", "name": "include-packages", "type": "text"},
                    ],
                },
                {
                    "name": "node-details",
                    "title": "List details for a node",
                    "mode": "detail",
                    "params": [
                        {"title": "Filter", "name": "filter", "type": "text", "required": True},
                    ],
                },
                {
                    "name": "running-models-paste",
                    "title": "List running models (Paste logs)",
                    "mode": "filter",
                    "params": [
                        {"title": "File", "name": "file", "type": "text"},
                    ],
                },
                {
                    "name": "running-models-file",
                    "title": "List running models (Read logs from file)",
                    "mode": "filter",
                    "params": [
                        {"title": "Dir", "name": "dir", "type": "text"},
                        {"title": "Show Hidden", "name": "show-hidden", "type": "text"},
                    ],
                },
            ],
        },
        sys.stdout,
        indent=4,
    )
    sys.exit(0)

payload = json.loads(sys.argv[1])

if payload["command"] == "run-results":
    work_dir = "."
    incl_packages = (
        payload["params"]["include-packages"] if "include-packages" in payload["params"] else False
    )
    run_results.execute(dir=work_dir, include_packages=incl_packages)

if payload["command"] == "node-details":
    work_dir = "."
    filter = payload["params"]["filter"]
    node_details.execute(dir=work_dir, filter=filter)

if payload["command"] == "running-models-paste":
    running_models.execute(input_type="paste")

if payload["command"] == "running-models-file":
    work_dir = "."
    running_models.execute(input_type="file", dir=work_dir)
