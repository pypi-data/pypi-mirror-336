# uvxship

**Build → Publish → Release** for Python projects using `uv`.

## Features

- `uvx build`  : cleans `dist/` and runs `uv build`
- `uvx publish`: uses `~/.pypirc` to upload to PyPI
- `uvx ship`   : combines both in one go

## Why?

Because `uv publish` doesn't yet support `~/.pypirc`. This fills the gap.
And PYPI rejects `uv publish` in the second try because `dist/` contains older release packages.
The "fix" is to clean `dist/` before every `uv build`. And to wrap `uv publish` with a
parser for `~/.pypirc` to lookup the credentials.
This smoothens the releasing/shipping of packages with `uv`.

So with a single command
```
uvx ship
```
you
1. clean the `dist/` folder
2. `uv build` the package
3. `uv publish` the package to PYPI or with `--repository testpypi` to test PYPI
   or other repositories when specified in the `~/.pypirc` file.
4. arguments passed to `uvx ship` are forwarded to `uv publish`.

CAVE!
```
uv pip install uvxship
pip install uvxship
```
does NOT make these `uvx` commands available!
Only a `uv tool install uvxship` leads to the desired result!

## Install By `uv`
```bash
uv tool install uvxship
```

## Or Install Locally

```bash
git clone
uv tool install -e .    # or `uv tool install -e path/to/uvxship` 
```
This is like `uv pip install -e .` and installs 
the package to `uv tool` in editable mode.

## Usage
```bash
uvx build
uvx publish
```
or a single
```bash
uvx ship
```
additional arguments to `uvx ship` are passed down to `uv publish`:
```bash
uvx ship --repository testpypi
```
This
- cleans the `dist/` file in the background
- calls `uv build`
- parses `~/.pypirc` for PYPI credentials
  (you have to set it up yourself)
- and publishes `uv publish --repository testpypi`
