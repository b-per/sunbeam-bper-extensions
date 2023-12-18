#!/usr/bin/env python3

# using urllib to not require requests
import json
import common
from common import Requests, ts_to_datetime, run_duration

from asciichartpyx import plot

DAGSTER_URL = common.DAGSTER_URL
HEADERS = common.HEADERS


def execute(command, filter=None):
    dagster_request = Requests(f"{DAGSTER_URL}/graphql", HEADERS)

    if command == "list-assets":
        last_mater_all_assets = """
        query lastMaterialization {
            assetsOrError {
                ...on AssetConnection {
                nodes {
                    key {
                        path
                    }
                assetMaterializations(limit:1) {
                    timestamp
                }
                }
                }
            }
        }
        """

        response = dagster_request.post(
            dict_data={"query": last_mater_all_assets},
        )

        ret = {
            "items": [
                {
                    "title": ".".join(asset_mater["key"]["path"]),
                    "subtitle": ts_to_datetime(
                        asset_mater["assetMaterializations"][0]["timestamp"], ms=True
                    )
                    if asset_mater["assetMaterializations"]
                    else "",
                    "actions": [
                        {
                            "title": "List All Materializations",
                            "key": "m",
                            "type": "run",
                            "command": "last-mater-single-asset",
                            "params": {"filter": ".".join(asset_mater["key"]["path"])},
                        },
                        {
                            "title": "Plot Materialization Time",
                            "key": "p",
                            "type": "run",
                            "command": "plot-asset-mater",
                            "params": {"filter": ".".join(asset_mater["key"]["path"])},
                        },
                    ],
                }
                for asset_mater in response["data"]["assetsOrError"]["nodes"]
            ],
        }

        print(json.dumps(ret, indent=2))

    elif command == "last-mater-single-asset":
        last_maters_single_asset = """
        query myquery($assetKey: AssetKeyInput!) {
            assetOrError(assetKey: $assetKey) {
                __typename
                ... on Asset {
                id
                assetMaterializations(limit: 100) {
                    runId
                    partition
                    message
                    stepKey
                    timestamp
                    stepStats {
                    status
                    startTime
                    endTime
                    }
                        eventType
                        metadataEntries {
                        label
                        __typename
                        ... on FloatMetadataEntry {
                            floatValue
                        }
                    }
                }
                assetObservations {
                    runId
                }
                }
            }
        }
        """

        response = dagster_request.post(
            dict_data={
                "query": last_maters_single_asset,
                "variables": {"assetKey": {"path": filter.split(".")}},
            },
        )

        ret = {
            "items": [
                {
                    "title": ("✅ " if asset_mater["stepStats"]["status"] == "SUCCESS" else "❌ ")
                    + asset_mater["runId"]
                    + " - "
                    + asset_mater["stepKey"],
                    # "subtitle": f"""Ran in {asset_mater["stepStats"]["endTime"] - asset_mater["stepStats"]["startTime"]} secs""",
                    "subtitle": f"""{ts_to_datetime(asset_mater["timestamp"], ms=True)}""",
                    "accessories": [f"""{run_duration(asset_mater)} secs"""],
                    "actions": [
                        {
                            "title": "Check run on Dagster",
                            "key": "m",
                            "type": "open",
                            "url": f"""{DAGSTER_URL}/runs/{asset_mater["runId"]}""",
                        },
                        {
                            "title": "Copy URL",
                            "key": "y",
                            "type": "copy",
                            "text": f"""{DAGSTER_URL}/runs/{asset_mater["runId"]}""",
                        },
                    ],
                }
                for asset_mater in response["data"]["assetOrError"]["assetMaterializations"]
            ],
        }

        print(json.dumps(ret, indent=2))

    elif command == "plot-asset-mater":
        last_maters_single_asset = """
        query myquery($assetKey: AssetKeyInput!) {
            assetOrError(assetKey: $assetKey) {
                __typename
                ... on Asset {
                id
                assetMaterializations(limit: 100) {
                    runId
                    partition
                    message
                    stepKey
                    timestamp
                    stepStats {
                    status
                    startTime
                    endTime
                    }
                        eventType
                        metadataEntries {
                        label
                        __typename
                        ... on FloatMetadataEntry {
                            floatValue
                        }
                    }
                }
                assetObservations {
                    runId
                }
                }
            }
        }
        """

        response = dagster_request.post(
            dict_data={
                "query": last_maters_single_asset,
                "variables": {"assetKey": {"path": filter.split(".")}},
            },
        )

        myx = [
            ts_to_datetime(asset_mater["timestamp"], ms=True)[:10]
            for asset_mater in response["data"]["assetOrError"]["assetMaterializations"]
        ][::-1]
        myy = [
            int(float(run_duration(asset_mater)))
            for asset_mater in response["data"]["assetOrError"]["assetMaterializations"]
        ][::-1]

        config = {
            "title": "Time to generate asset",
            "height": 10,
            "width": 90,
            "line_labels": [
                "time (secs)",
            ],
            "x_label": "date",
            "y_label": "time",
            "x_array": myx,
            "format": "{:4.0f}",
        }

        ret = {"text": f"{plot([myy], config)}", "highlight": "ansi"}

        print(json.dumps(ret, indent=2))
