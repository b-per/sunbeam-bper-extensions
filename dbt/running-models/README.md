# running-models

## installation

```bash
sunbeam extension install dbtrm ...
```

This extension requires reading from the clipboard. It will try to use `pyperclip` if it is installed, and otherwise will fallback to `pbpaste` for MacOS.

For Windows/Linux, you will currently need to have `pyperclip` installed in your main Python environment.

## usage

- copy the dbt logs into your clipboard
- run `sunbeam dbtrm`
- enjoy
