# check-depz: Easy outdated dependencies check for Python projects 

Project `check-depz` is a simple command line tool to easily check if your Python project contains too many outdated dependencies. 

## Usage

Add `check-depz` to your project:

```
$ poetry add --group=dev check-depz 
```

Run dependencies check:

```
$ poetry run check-depz
Number of outdated dependencies: 0
Dependency check passed.
```

### Outdated dependencies limit 

By default `check-depz` allow up to 10 outdated dependencies.

### Exit codes

Please note `check-depz` returns exit code `0` on succesfull check and code `1` on failure, so you can rely on this behavior:

```
check-depz && echo "Dependencies are up to date!"
```

...or...


```
#!/bin/bash
set -e  # Exit on command failure

check-depz
echo "This will NOT run if there are too many out of date dependencies."

```