# sunbeam-bper-extensions

This is a collection of [sunbeam](https://github.com/pomdtr/sunbeam) extensions built for my own use cases but which could be reused by the community.

Sunbeam is a great cross platform tool to build Terminal UIs based on JSON inputs

## requirements

- [install sunbeam](https://pomdtr.github.io/sunbeam/book/#installation-1)
  - the current repository has been tested on `v1.0.0-rc.56` and there might be breaking changes before the final `v1`
- install the different extensions with `sunbeam extension install --alias <alias> <url_or_path>`

## additional information

- some commands require Python installed (out of the box on MacOS but needs to be installed separately on Windows)
- some commans require `bash` and will most likely not work on Windows
- some commands require having environment variables set in `~/.sunbeamrc`. for those, an example is provided in the folder to list the env variables that need to be set
