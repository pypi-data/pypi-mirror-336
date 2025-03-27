# check-dependencies: Easy outdated dependencies check for Python projects 

Project `check-dependencies` is a simple command line tool to easily check if your Python project contains too many outdated dependencies. 

## Usage

Add `check-dependencies` to your project:

```
$ poetry add --group=dev git+https://github.com/hekonsek/check-dependencies.git@v0.4.0 
```

Run dependencies check:

```
$ poetry run check-dependencies
Number of outdated dependencies: 0
Dependency check passed.
```

### Outdated dependencies limit 

By default `check-dependencies` allow up to 10 outdated dependencies.

### Exit codes

Please note `check-dependencies` returns exit code `0` on succesfull check and code `1` on failure, so you can rely on this behavior:

```
check-dependencies && echo "Dependencies are up to date!"
```

...or...


```
#!/bin/bash
set -e  # Exit on command failure

check-dependencies
echo "This will NOT run if there are too many out of date dependencies."

```