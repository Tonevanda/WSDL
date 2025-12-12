# WSDL

## Installation

To run the project, you need uv. You can follow the installation process [here](https://docs.astral.sh/uv/getting-started/installation/).

The dataset can be found [here](https://datarepositorium.uminho.pt/dataset.xhtml?persistentId=doi:10.34622/datarepositorium/K1DQIT) and should be placed under ``/resources/bulk``

## Running

First, to create/update your virtual environment with the desired packages, run:

```sh
uv sync
```

Then run:

```sh
uv run python src/main.py
```