# sunbeam-bper-extensions

This is a collection of [sunbeam](https://github.com/pomdtr/sunbeam) extensions built for my own use cases but which could be reused by the community.

Sunbeam is a great cross platform tool to build Terminal UIs based on JSON inputs

## requirements

- [install sunbeam](https://pomdtr.github.io/sunbeam/book/#installation-1)
  - the current repository has been based on `v1.0.0-rc.19` and it is expected that there will be breaking changes before the final `v1`
- install the different extensions with `sunbeam extension install <cmd_name> <ulr_or_path>`

## additional information

- some commands require Python installed (out of the box on MacOS but needs to be installed separately on Windows)
- some commans require `bash` and will most likely not work on Windows
- some commands require having environment variables set. for those, a `.envrc.example` is provided to list the env variables that need to be set
