# ![PaxDeiLogo](https://playpaxdei.com/_next/image?url=%2Fstatic%2Fimages%2Fpaxdei-monogram-silver.png&w=64&q=75 "Get it?") Paxo - development utilities for PaxDei

## Introduction

This is a collection of scripts and tools to facilitate the development process
of PaxDei using a command line utility.  The philosophy is that a regular developer can perform most complex development tasks using a single command
line utility.  The utility can then be updated and expanded as needs arise.

Tasks that can be performed include

- *initial-setup*:  Installing necessary tools, p4, setting up workspaces, syncing
- *sync*: perforce sync of a branch
- *work-in*: switching branches
- *update*: update the utility

## Installing

The only pre-requisite for running paxo is having [uv](https://docs.astral.sh/uv/) installed. To install, simply type

`uv tool install mainframe-paxo`

This installation can be automated performed by a script which exists on `"G:\Shared drives\devex\paxo\install.cmd"` which will install the necessary pre-requisites, fetch paxo and run `paxo basic-install`.
the `install.cmd` script is also available here, in `install.cmd`.

## Usage

type `paxo --help` for instructions.

## Development

We use [uv](https://docs.astral.sh/uv/) for development.  Install uv as per instructions on site.

To run the command line, use something like:

`uv run python -m mainframe_paxo.paxo p4 ...`

### set up

run `uv sync` to set up a develoment env.

### publishing

To publish, the package version needs to be upgraded.  You then
run `uv build` and `uv publish` to publish this to PyPI.

First, though, you need to get the PyPI access token.  It is in OnePass.

The steps are:

1. update the version in `pyproject.toml`
2. delete the contents of the `dist` folder
2. `uv build`
4. `uv publish --token <token>

### updating

To update an installed client to the latest version from PyPI, type
`uv tool upgrade mainframe-paxo`