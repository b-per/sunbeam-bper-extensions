# run-results

This command displays the list of models/tests that were run as part of the last dbt command and sort them by first showing the errors and then listing the nodes by the time they took to run.

## installation

```bash
sunbeam extension install dbtrr ...
```

## usage

- go to the root folder of your dbt project where you ran dbt rencently
- run `sunbeam dbtrr`
  - or run `sunbeam dbtrr --include-packages` to include packages (excluded by default)
- pressing `tab` then shows a submenu where you can naviagte to the model/YAML or see some details about the model
