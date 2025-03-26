# GFW API Python Client

<!-- start: badges -->
[![ci](https://github.com/GlobalFishingWatch/gfw-api-python-client/actions/workflows/ci.yaml/badge.svg)](https://github.com/GlobalFishingWatch/gfw-api-python-client/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/GlobalFishingWatch/gfw-api-python-client/branch/develop/graph/badge.svg?token=w4R4VZB5RY)](https://codecov.io/gh/GlobalFishingWatch/gfw-api-python-client)
[![license](https://img.shields.io/badge/license-Apache%202-blue)](https://github.com/GlobalFishingWatch/gfw-api-python-client/blob/main/LICENSE)

[![pre-commit action](https://github.com/GlobalFishingWatch/gfw-api-python-client/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/GlobalFishingWatch/gfw-api-python-client/actions/workflows/pre-commit.yaml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![conventional commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
<!-- end: badges -->

Python package for accessing data from Global Fishing Watch (GFW) APIs.

> **Important:**
This version of `gfw-api-python-client` gives access to Global Fishing Watch API [version 3](https://globalfishingwatch.org/our-apis/documentation#version-3-api). Starting April 30th, 2024, this is the official API version. For latest API releases, please check our [API release notes](https://globalfishingwatch.org/our-apis/documentation#api-release-notes)


The `gfw-api-python-client` is a simple wrapper for the Global Fishing Watch (GFW) [APIs](https://globalfishingwatch.org/our-apis/documentation#introduction). It provides convenient functions to freely pull GFW data.

The package currently works with the following APIs:

- [Vessels API](https://globalfishingwatch.org/our-apis/documentation#vessels-api): vessel search and identity based on AIS self reported data and public registry information

- [Events API](https://globalfishingwatch.org/our-apis/documentation#events-api): encounters, loitering, port visits, AIS-disabling events and fishing events based on AIS data

- [Gridded fishing effort (4Wings API)](https://globalfishingwatch.org/our-apis/documentation#map-visualization-4wings-api): apparent fishing effort based on AIS data

> **Note**: See the [Terms of Use](https://globalfishingwatch.org/our-apis/documentation#reference-data) page for GFW APIs for information on our API licenses and rate limits.

## Installation

You can install the most recent version of `gfw-api-python-client` using:

```sh
pip install gfw-api-python-client
```

Once everything is installed you can load and use `gfw-api-python-client` in your `codes`, `scripts`, `notebooks` etc., using:

```python
from gfwapiclient import Client

gfw = Client(api_token="<PASTE_YOUR_TOKEN_HERE>")
```

## Authorization

The use of `gfw-api-python-client` requires a GFW API token, which users can request from the [GFW API Portal](https://globalfishingwatch.org/our-apis/tokens). Save this token to your `.env` by adding a variable named `GFW_API_TOKEN` i.e., (`GFW_API_TOKEN="PASTE_YOUR_TOKEN_HERE"`) and save the `.env` file.

```.env
GFW_API_TOKEN=<PASTE_YOUR_TOKEN_HERE>
```

## Contributing

We welcome all contributions to improve the package!. Please read our [Contribution Guide](https://github.com/GlobalFishingWatch/gfw-api-python-client/blob/main/Contributing.md) and reach out!.
