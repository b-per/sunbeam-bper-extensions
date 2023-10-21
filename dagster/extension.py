import sys
import json
import pathlib

import dagster_assets
import dagster_runs


if len(sys.argv) == 1:
    json.dump(
        {
            "title": "Dagster",
            "commands": [
                {
                    "name": "list-assets",
                    "title": "List Assets",
                    "mode": "view",
                },
                {
                    "name": "last-mater-single-asset",
                    "title": "Last Materializations for the asset",
                    "mode": "view",
                    "params": [
                        {"name": "filter", "type": "string", "required": True},
                    ],
                },
                {
                    "name": "plot-asset-mater",
                    "title": "Plot Materialization time for the asset",
                    "mode": "view",
                    "params": [
                        {"name": "filter", "type": "string", "required": True},
                    ],
                },
                {
                    "name": "list-runs",
                    "title": "Last Runs in Dagster",
                    "mode": "view",
                },
            ],
        },
        sys.stdout,
        indent=4,
    )
    sys.exit(0)

if sys.argv[1] == "list-assets":
    payload = json.load(sys.stdin)
    dagster_assets.execute(command="list-assets")

if sys.argv[1] == "last-mater-single-asset":
    payload = json.load(sys.stdin)
    filter = payload["params"]["filter"]
    dagster_assets.execute(command="last-mater-single-asset", filter=filter)

if sys.argv[1] == "plot-asset-mater":
    payload = json.load(sys.stdin)
    filter = payload["params"]["filter"]
    dagster_assets.execute(command="plot-asset-mater", filter=filter)

if sys.argv[1] == "list-runs":
    payload = json.load(sys.stdin)
    dagster_runs.execute()
