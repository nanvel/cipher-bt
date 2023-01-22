# FAQ

## How to have a single open session

In most cases, opening a new session, while there are other open sessions, is desirable.

If we don't want to start a new session while there are open sessions:
```python
def on_entry(self, row, session):
    if self.wallet.base != 0:
        # we still hold a position for an open session
        return
    ...
```
