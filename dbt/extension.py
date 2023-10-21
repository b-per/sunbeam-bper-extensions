import sys
import json
import pathlib

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
                    "mode": "view",
                    "params": [
                        {"name": "include-packages", "type": "boolean"},
                    ],
                },
                {
                    "name": "node-details",
                    "title": "List details for a node",
                    "mode": "view",
                    "params": [
                        {"name": "filter", "type": "string", "required": True},
                    ],
                },
                {
                    "name": "running-models-paste",
                    "title": "List running models (Paste logs)",
                    "mode": "view",
                    "params": [
                        {"name": "fil", "type": "boolean"},
                    ],
                },
                {
                    "name": "running-models-file",
                    "title": "List running models (Read logs from file)",
                    "mode": "view",
                    "params": [
                        {"name": "dir", "type": "string"},
                        {"name": "show-hidden", "type": "boolean"},
                    ],
                },
            ],
        },
        sys.stdout,
        indent=4,
    )
    sys.exit(0)

if sys.argv[1] == "run-results":
    payload = json.load(sys.stdin)
    work_dir = payload["cwd"]
    run_results.execute(dir=work_dir)

if sys.argv[1] == "node-details":
    payload = json.load(sys.stdin)
    work_dir = payload["cwd"]
    filter = payload["params"]["filter"]
    node_details.execute(dir=work_dir, filter=filter)

if sys.argv[1] == "running-models-paste":
    payload = json.load(sys.stdin)
    work_dir = payload["cwd"]
    running_models.execute(input_type="paste")

if sys.argv[1] == "running-models-file":
    payload = json.load(sys.stdin)
    work_dir = payload["cwd"]
    running_models.execute(input_type="file", dir=work_dir)
