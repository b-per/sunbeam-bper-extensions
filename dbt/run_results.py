import json
import sys
from pathlib import Path
from datetime import datetime
import yaml


def execute(dir, include_packages=False):
    run_results_file_path = dir / Path("target/run_results.json")
    run_results = json.loads(run_results_file_path.read_text())

    manifest_file_path = dir / Path("target/manifest.json")
    manifest = json.loads(manifest_file_path.read_text())

    dbt_project_file = dir / Path("dbt_project.yml")
    dbt_project_name = yaml.safe_load(dbt_project_file.read_text())["name"]

    def show_status(result: dict) -> str:
        status = result["status"]
        if status in ["success", "pass"]:
            return f"{status} ✅"
        if status in ["warn"]:
            return f"{status} 🚧"
        if status in ["skipped"]:
            return f"{status} 🦘"
        else:
            return f"{status} ❌"

    def execute_time_int(result: dict) -> int:
        if len(result["timing"]) < 2:
            return 999_999
        end_time = datetime.fromisoformat(result["timing"][1]["completed_at"].rstrip("Z"))
        start_time = datetime.fromisoformat(result["timing"][1]["started_at"].rstrip("Z"))
        return int((end_time - start_time).total_seconds())

    def execute_time_seconds(result: dict) -> str:
        execute_time = execute_time_int(result)
        if execute_time == 999_999:
            return ""
        else:
            return "{:,}".format(execute_time) + " secs"

    def number_rows(result: dict) -> str:
        if "rows_affected" not in result["adapter_response"]:
            return "-"

        rows_adapter = result["adapter_response"]["rows_affected"]
        if rows_adapter in [0, 1]:
            return "N/A"

        return "{:,}".format(result["adapter_response"].get("rows_affected", "-")) + " rows"

    def show_unique_id(result: dict) -> str:
        unique_id = result["unique_id"]
        unique_id_model, unique_id_package, unique_id_node, *extra = unique_id.split(".")
        return f"{unique_id_model[0].upper()}: {unique_id_node}"

    list_rows = []
    for result in sorted(run_results["results"], key=execute_time_int, reverse=True):
        if result["unique_id"].split(".")[1] != dbt_project_name and not include_packages:
            continue

        row = {}
        actions = []
        row["title"] = show_unique_id(result)
        row["subtitle"] = show_status(result)
        row["accessories"] = [execute_time_seconds(result), number_rows(result)]

        actions.append(
            {
                "title": "Copy Name",
                "key": "y",
                "onAction": {
                    "type": "copy",
                    "text": result["unique_id"].split(".")[-1],
                },
            }
        )

        if Path(manifest["nodes"][result["unique_id"]]["original_file_path"]).exists():
            actions.append(
                {
                    "title": "Open file",
                    "key": "o",
                    "onAction": {
                        "type": "open",
                        "target": manifest["nodes"][result["unique_id"]]["original_file_path"],
                    },
                }
            )

        compiled_path = manifest["nodes"][result["unique_id"]].get("compiled_path")
        if compiled_path and Path(compiled_path).exists():
            actions.append(
                {
                    "title": "Open compiled code",
                    "key": "c",
                    "onAction": {
                        "type": "open",
                        "target": manifest["nodes"][result["unique_id"]]["compiled_path"],
                    },
                }
            )

        patch_path = manifest["nodes"][result["unique_id"]]["patch_path"]
        if patch_path:
            yml_file = patch_path.split("://")[-1]
            if yml_file and Path(yml_file).exists():
                actions.append(
                    {
                        "title": "Open YAML",
                        "key": "c",
                        "onAction": {
                            "type": "open",
                            "target": yml_file,
                        },
                    }
                )

        actions.append(
            {
                "title": "See details",
                "key": "d",
                "onAction": {
                    "type": "run",
                    "command": "node-details",
                    "params": {"filter": result["unique_id"]},
                },
            }
        )

        row["actions"] = actions
        list_rows.append(row)

    json.dump(
        {
            "type": "list",
            "items": list_rows,
        },
        sys.stdout,
    )
