from datetime import datetime
import urllib.request
import json
import os


DAGSTER_URL = os.environ.get("SB_DAGSTER_URL")
DAGSTER_EXTRA_HEADERS = json.loads(os.environ.get("SB_DAGSTER_EXTRA_HEADERS", "{}"))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Connection": "keep-alive",
}

for extra_header_name, extra_header_val in DAGSTER_EXTRA_HEADERS.items():
    HEADERS[extra_header_name] = extra_header_val


# to avoid having to install requests
class Requests:
    def __init__(self, url, headers) -> None:
        self.url = url
        self.headers = headers

    def post(self, dict_data) -> dict:
        data_json = json.dumps(dict_data).encode()
        req = urllib.request.Request(self.url, data=data_json, headers=self.headers)

        try:
            with urllib.request.urlopen(req) as response:
                response_text = response.read()
                try:
                    response_data = json.loads(response_text)
                except json.decoder.JSONDecodeError as e:
                    exit(f"JSONDecodeError: {e} -- Text: {response_text}")
        except urllib.error.HTTPError as e:
            # Handle error here
            exit(f"HTTPError: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            # Handle error here
            exit(f"URLError: {e.reason}")

        return response_data


def ts_to_datetime(ts, ms=False):
    if ms:
        return datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%d %H:%M")
    else:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")


def run_duration(materialization):
    dbt_metadata_entries = metadata_entries_dbt(materialization["metadataEntries"])
    if dbt_metadata_entries:
        return dbt_metadata_entries
    else:
        return format(
            materialization["stepStats"]["endTime"]
            - materialization["stepStats"]["startTime"],
            ".1f",
        )


def metadata_entries_dbt(metadata_entries):
    values = [
        meta["floatValue"]
        for meta in metadata_entries
        if meta["__typename"] == "FloatMetadataEntry"
    ]
    return format(values[0], ".1f") if values else None
