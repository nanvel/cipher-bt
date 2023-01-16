# Installation

## Local

Requirement: Python 3.8+

```shell
python --version
# Python 3.10.8
```

Create a directory for your strategies:
```shell
mkdir strategies
cd strategies
```

Create a Python virtual environment and activate it:
```shell
python -m venv .venv
source .venv/bin/activate
```

Install Cipher:
```shell
pip install cipher-bt[finplot]
```

Initialize the directory and create a strategy:
```shell
cipher init
cipher new my_strategy
```

Run the strategy:
```shell
python my_strategy.py
```

## Google Colaboratory

```text
!pip install cipher-bt
```
