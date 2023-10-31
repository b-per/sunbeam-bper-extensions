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
                    "mode": "list",
                },
                {
                    "name": "last-mater-single-asset",
                    "title": "Last Materializations for the asset",
                    "mode": "list",
                    "params": [
                        {"name": "filter", "type": "string", "required": True},
                    ],
                },
                {
                    "name": "plot-asset-mater",
                    "title": "Plot Materialization time for the asset",
                    "mode": "detail",
                    "params": [
                        {"name": "filter", "type": "string", "required": True},
                    ],
                },
                {
                    "name": "list-runs",
                    "title": "Last Runs in Dagster",
                    "mode": "list",
                },
            ],
        },
        sys.stdout,
        indent=4,
    )
    sys.exit(0)

input = json.loads(sys.argv[1])

if input["command"] == "list-assets":
    dagster_assets.execute(command="list-assets")

if input["command"] == "last-mater-single-asset":
    filter = input["params"]["filter"]
    dagster_assets.execute(command="last-mater-single-asset", filter=filter)

if input["command"] == "plot-asset-mater":
    filter = input["params"]["filter"]
    dagster_assets.execute(command="plot-asset-mater", filter=filter)

if input["command"] == "list-runs":
    dagster_runs.execute()
