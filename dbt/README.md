# dbt

This extension provides some help to parse JSON dbt artefacts. It contains a set of 4 subcommands

```
Available Commands:
  node-details         List details for a node
  run-results          List models run
  running-models-file  List running models (Read logs from file)
  running-models-paste List running models (Paste logs)
```

## Installation

```bash
sunbeam extension install https://raw.githubusercontent.com/b-per/sunbeam-bper-extensions/main/dbt
```

## run-results

- go to the root folder of your dbt project where you ran dbt rencently
- run `sunbeam dbt run-results`
  - or run `sunbeam run-results --include-packages` to include packages (excluded by default)
- pressing `tab` then shows a submenu where you can navigate to the model/YAML or see some details about the model

## running-models-file

- run your dbt command and add `| tee dbt.stdout` at the end (e.g. `dbt run | tee dbt.stdout`)
- in the root folder of your dbt project, run `sunbeam dbt running-models-file` (or `sunbeam dbt` and select the correct entry)
- press `Enter` to refresh the list of models/tests currently running
- enjoy

## running-models-paste

- copy the dbt logs into your clipboard
- run `sunbeam dbt running-models-paste`
- enjoy
