# Cipher - trading strategy backtesting framework

Development:
```shell
brew install poetry
poetry init
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
