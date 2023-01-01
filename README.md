# Cipher - trading strategy backtesting framework

![Tests](https://github.com/nanvel/cipher-bt/actions/workflows/tests.yml/badge.svg)

Development:
```shell
brew install poetry
poetry install
poetry shell

pytest tests

cipher --help
```

Initialize a new strategies folder and create a strategy:
```bash
mkdir my_strategies
cd my_strategies

cipher init
cipher new my_strategy
python my_strategy.py
```
