# running-models

## installation

```bash
sunbeam extension install dbtrmf https://raw.githubusercontent.com/b-per/sunbeam-bper-extensions/main/dbt/running-models-file/sunbeam-extension
```

## demo

[Loom](https://www.loom.com/share/7441838e3b4f40019cb9422794587f4d?sid=0d1384e8-ab34-4a99-a4d8-5a4e3c67e007)

## usage

- run your dbt command and add `| tee dbt.stdout` at the end (e.g. `dbt run | tee dbt.stdout`)
- in the root folder of your dbt project, run `sunbeam dbtrmf`
- presee `Enter` to refresh the list of models/tests curretnyl running
- enjoy
