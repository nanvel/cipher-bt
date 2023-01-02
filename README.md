# Cipher - backtesting framework

```mermaid
graph TD;
    Log-->Broker;
    Log-->Visualize;
    Log-->Stats;
    Wallet-->Broker;
    Trade-->Broker;
    Broker-->Engine;
    Strategy-->Engine;
    Data-->Engine;
    Source-->Data;
    Data-->Stats;
    Data-->Visualize;
```
