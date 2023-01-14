# Cipher - trading strategy backtesting framework

![Tests](https://github.com/nanvel/cipher-bt/actions/workflows/tests.yaml/badge.svg)

Documentation: https://cipher.nanvel.com

## Usage

Initialize a new strategies folder and create a strategy:
```shell
pip install cipher-bt
mkdir my_strategies
cd my_strategies

cipher init
cipher new my_strategy
python my_strategy.py
```

## Development

```shell
brew install poetry
poetry install
poetry shell

pytest tests

cipher --help
```


