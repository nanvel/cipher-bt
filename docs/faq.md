# Strategy FAQ

## How to allow only one open session at a time

By default, the system allows multiple concurrent sessions. To restrict to a single open session, check if a position is already held before entering a new one:

```python
def on_entry(self, row, session):
    if self.wallet.base != 0:
        # Skip entry if we already hold a position from another session
        return
    # ... rest of your entry logic
```

## Why does Cipher truncate the dataframe?

Cipher automatically removes rows from the beginning of the dataframe when using indicators that require a warm-up period.

**Example:** If your dataframe includes an EMA50 indicator, the first 50 rows will contain null values since the indicator needs 50 data points to calculate meaningful results. Cipher removes these unusable rows to ensure your strategy only processes valid data.

## How to debug strategy code

Use Python's built-in debugger (`pdb`) to step through your code interactively:

```python
def compose(self):
    df = self.datas.df

    breakpoint()  # Execution will pause here for debugging

    return df
```
