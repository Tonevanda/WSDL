# WSDL

## Installation

To run the project, you need uv. You can follow the installation process [here](https://docs.astral.sh/uv/getting-started/installation/).

## Running

First, to create/update your virtual environment with the desired packages, run:

```sh
uv sync
```

Then run:

```sh
uv run python src/main.py
```

This will use our small Ontology developed in Protégé and complete it with Entities.

## Querying

Run

```sh
uv run python src/sparql.py
```