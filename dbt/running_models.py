#!/usr/bin/env python

from dataclasses import dataclass
from collections import Counter
import re
import sys
import json
from datetime import datetime
from pathlib import Path


# Example of input

"""
10:03:09  1 of 10 START sql table model hyrule.source_quests  [RUN]
10:03:19  1 of 10 OK created sql table model hyrule.source_quests  [SELECT in 10.78s]
10:03:09  2 of 10 START sql table model hyrule.source_fairies  [RUN]
10:03:09  3 of 10 START sql table model hyrule.source_rupees  [RUN]
10:03:09  4 of 10 START sql table model hyrule.source_rewards  [RUN]
10:03:09  5 of 10 START sql table model hyrule.dim_fairies  [RUN]
10:03:09  6 of 10 START sql table model hyrule.fct_quests  [RUN]
10:03:19  7 of 10 START sql table model hyrule.fct_rupees  [RUN]
10:03:23  2 of 10 OK created sql table model hyrule.source_fairies  [SELECT in 14.44s]
10:03:23  8 of 10 START sql table model hyrule.mart_weekly_quests  [RUN]
10:03:29  3 of 10 OK created sql table model hyrule.source_rupees  [SELECT in 20.14s]
10:03:29  9 of 10 START sql incremental model hyrule.mart_weekly_rewards  [RUN]
10:05:55  7 of 10 OK created sql table model hyrule.fct_rupees  [SELECT in 155.22s]
10:05:55  10 of 10 START sql incremental model hyrule.mart_worlds  [RUN]
10:06:33  8 of 10 OK created sql table model hyrule.mart_weekly_quests  [SELECT in 189.95s]
10:06:33  11 of 12 START sql table model hyrule.heart_matrix  [RUN]
10:07:32  9 of 10 OK created sql incremental model hyrule.mart_weekly_rewards  [SELECT in 243.76s]
10:08:00  12 of 12 START sql incremental model hyrule.triforce_purchases  [RUN]
10:08:35  12 of 12 ERROR creating sql incremental model hyrule.triforce_purchases  [ERROR in 17.03s]
"""


@dataclass
class LogLine:
    timecode: datetime
    model_num: int
    of: str
    total_models: int
    action: str
    materialization: str
    model_name: str
    status: str
    runtime_1: str = ""
    runtime_2: str = ""
    additional: str = ""

    def __post_init__(self):
        self.timecode = datetime.strptime(self.timecode, "%H:%M:%S")
        self.model_num = int(self.model_num)
        self.total_models = int(self.total_models)
        if self.action == "FAIL":
            self.materialization = "test"


def get_input_paste():
    try:
        import pyperclip  # type: ignore

        raw_input = pyperclip.paste()
    except ImportError:
        import subprocess

        raw_input = subprocess.check_output("pbpaste", universal_newlines=True)

    return raw_input.splitlines()


def get_input_file(dir):
    raw_input = (dir / Path("dbt.stdout")).read_text()
    return raw_input.splitlines()


def execute(input_type, dir="."):
    ansi_escape = re.compile(
        r"""
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    """,
        re.VERBOSE,
    )

    if input_type == "paste":
        input = get_input_paste()
    elif input_type == "file":
        input = get_input_file(dir)

    # Modify input by removing extraneous words -- this helps with string parsing later
    extraneous_words = [
        "sql ",
        "created ",
        "creating ",
        "model ",
        "loaded ",
        "file ",
        "in ",
        "VIEW ",
        "\.. ",
    ]

    for word in extraneous_words:
        input = [ansi_escape.sub("", re.sub(word, "", line)) for line in input]

    input = [re.sub("PASS ", "PASS test ", line) for line in input]

    log_lines = []

    for line in input:
        try:
            log_lines.append(LogLine(*line.split()))
        except:
            continue

    counter_models = Counter([line.model_num for line in log_lines])

    model_nums_not_finished = [
        model_num for model_num, count in counter_models.items() if count < 2
    ]
    models_not_finished = [
        model for model in log_lines if model.model_num in model_nums_not_finished
    ]

    if len(log_lines) > 0:
        message = "All models finished! 🎉"
    else:
        if input_type == "paste":
            message = "No valid logs were parsed, get the logs in your clipboard and try again."
        if input_type == "file":
            message = "No valid logs were parsed, is dbt tee-ing to `dbt.stdout`? \n\n If it is, dbt might still be warming up!"

    if len(models_not_finished) > -1:
        json.dump(
            {
                "title": "Models Not Finished 🦈",
                "emptyText": message,
                "actions": [
                    {
                        "title": "Refresh",
                        "type": "run",
                        "command": "running-models-file",
                    },
                ]
                if input_type == "file"
                else [],
                "items": [
                    {
                        "title": f"{model.model_num} - {model.model_name}",
                        "subtitle": str(model.timecode.time()),
                        "actions": [
                            action
                            for action in [
                                {
                                    "title": "Refresh",
                                    "type": "run",
                                    "command": "running-models-file",
                                }
                                if input_type == "file"
                                else None,
                                {
                                    "title": "Copy Name",
                                    "type": "copy",
                                    "text": model.model_name.split(".")[-1],
                                },
                            ]
                            if action is not None
                        ],
                    }
                    for model in sorted(models_not_finished, key=lambda x: x.model_num)
                ],
            },
            sys.stdout,
        )

    else:
        if len(log_lines) > 0:
            message = "All models finished! 🎉"
        else:
            if input_type == "paste":
                message = (
                    "No valid logs were parsed, get the logs in your clipboard and try again."
                )
            if input_type == "file":
                message = "No valid logs were parsed, is dbt tee-ing to `dbt.stdout`? \n\n If it is, dbt might still be warming up!"

        json.dump(
            {
                "type": "detail",
                "markdown": message,
                "actions": [
                    {
                        "title": "Refresh",
                        "onAction": {
                            "type": "run",
                            "command": "running-models-file",
                        },
                    },
                ]
                if input_type == "file"
                else [],
            },
            sys.stdout,
        )
