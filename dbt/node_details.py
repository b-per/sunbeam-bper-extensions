import json
import sys
from pathlib import Path


def execute(dir, filter):
    manifest_file_path = dir / Path("target/manifest.json")
    manifest = json.loads(manifest_file_path.read_text())

    node_id = filter
    node = manifest["nodes"][node_id]
    node_config = node["config"]

    newline = "\n"

    if node["resource_type"] in ["model", "snapshot", "seed"]:
        list_depends_on = []
        for depends_on_node in node.get("depends_on", {}).get("nodes", []):
            # only show the nodes for now
            if depends_on_node in manifest["nodes"]:
                list_depends_on.append(
                    f"""  - {depends_on_node} -- {manifest["nodes"][depends_on_node]["config"].get("materialized")}"""
                )

        tests_for_model = [
            test
            for test, test_values in manifest["nodes"].items()
            if test_values["resource_type"] == "test"
            and node_id in test_values["depends_on"]["nodes"]
        ]
        tests_to_print = ["  - " + test for test in tests_for_model]

        details = f"""
Model: {node_id}

Config:
  - Materialization: {node_config["materialized"]}
  - Has YAML: {"Yes" if node["patch_path"] else "No"}
  - Group: {node_config.get("group","N/A")}
  - Schema: {node_config["schema"]}
  - Alias: {node_config["alias"]}
  - Pre-hook: {"Yes" if node_config["pre-hook"] else "No"}
  - Post-hook: {"Yes" if node_config["post-hook"] else "No"}
  - Meta: {node_config["meta"]}
  - Contract: {node_config.get("contract","N/A")}
  - Constraints: {node_config.get("constraints","N/A")}

Depends on models:
{newline.join(list_depends_on)}

Tests:
{newline.join(tests_to_print) if tests_to_print else "  - None"}
"""

        ret = {"title": "Model details", "text": details}

    elif node["resource_type"] == "test":
        details = f"""
Test: {node_id}

Config:
  - Severity: {node_config["severity"]}
  - Schema: {node_config["schema"]}
"""

        ret = {"text": details}

    json.dump(
        ret,
        sys.stdout,
    )
