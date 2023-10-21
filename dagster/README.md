# dagster 

This extension queries the [Dagster](https://dagster.io/) GraphQL API to retrieve information from runs and assets.

It is currently more of a POC than a full featured tool. Issues/ideas/PRs are welcome.

The code uses standard Python without any external dependency (so, no `requests`) to make it easy for anyone to install.


# installation

```bash
sunbeam extension install --alias dagster github:b-per/sunbeam-bper-extensions/dagster
```

# configuration

Two environament variables can be made available in `~/.sunbeamrc` to connecto the API.

- `SB_DAGSTER_URL`: the URL of the Dagster instance
- `SB_DAGSTER_EXTRA_HEADERS`: a JSON string to add to the Headers of the HTTP requests 
(in my example, I used specific headers to access) a Dagster instance behind CloudFlare

An example of commands to add to `~/.sunbeamrc` is shown in the folder.

# usage

Run `sunbeam dagster` to see all the commands available or directly select one of the subcommands, like `list-assets` or `list-runs`.


# demo

[![asciicast](https://asciinema.org/a/4O7e3EKbdTdIXMUk37vMlQsra.svg)](https://asciinema.org/a/4O7e3EKbdTdIXMUk37vMlQsra)