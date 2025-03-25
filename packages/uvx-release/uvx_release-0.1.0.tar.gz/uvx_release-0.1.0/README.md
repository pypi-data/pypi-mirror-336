# uvx-release

**Build → Publish → Release** for Python projects using `uv`.

## Features

- `uvx build`: cleans `dist/` and runs `uv build`
- `uvx publish`: uses `~/.pypirc` to upload to PyPI
- `uvx release`: combines both in one go

## Why?

Because `uv publish` doesn't yet support `~/.pypirc`. This fills the gap.
And PYPI rejects `uv publish` because `dist/` contains older release packages.

## Install By `uv`
```bash
uv pip install uvx-release
```

## Or Install Locally

```bash
git clone
uv pip install -e .
```

## Usage
```bash
uvx build
uvx publish
```
or a single
```bash
uvx release
```
additional arguments to `uvx release` are passed down to `uv publish`:
```bash
uvx release --repository testpypi
```
This
- cleans the `dist/` file in the background
- calls `uv build`
- parses `~/.pypirc` for PYPI credentials
  (you have to set it up yourself)
- and publishes `uv publish --repository testpypi`
