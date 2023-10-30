#!/usr/bin/env /Users/bper/miniconda3/bin/python

import json
from datetime import datetime

import common
from common import Requests, ts_to_datetime


def metadata_entries_dbt(metada_entries):
    values = [
        meta["floatValue"] for meta in metada_entries if meta["__typename"] == "FloatMetadataEntry"
    ]
    return format(values[0], ".1f") if values else None


DAGSTER_URL = common.DAGSTER_URL
HEADERS = common.HEADERS


def execute():
    last_runs = """
    query runsOrError {
    runsOrError(limit: 200) {
        __typename
        ... on Runs {
        results {
            id
            status
            jobName
            startTime
            endTime
        }
        }
    }
    }
    """

    dagster_request = Requests(f"{DAGSTER_URL}/graphql", HEADERS)

    response = dagster_request.post(
        dict_data={"query": last_runs},
    )

    ret = {
        "title": "Last runs",
        "type": "list",
        "items": [
            {
                "title": ("✅ " if job_result["status"] == "SUCCESS" else "❌ ")
                + job_result["jobName"],
                "subtitle": f"""{ts_to_datetime(job_result["startTime"])}""",
                "accessories": [
                    f"""{format(job_result["endTime"] - job_result["startTime"],".1f")} secs"""
                ],
                "actions": [
                    {
                        "title": "Check run on Dagster",
                        "key": "m",
                        "type": "open",
                        "target": f"""{DAGSTER_URL}/runs/{job_result["id"]}""",
                    }
                ],
            }
            for job_result in response["data"]["runsOrError"]["results"]
        ],
    }

    print(json.dumps(ret, indent=2))
