# Time Shift

A simple Python utility to create lagged and lead variables for panel or time series data.

## Installation

```bash
pip install scicraft
```

## Usage

```python
from scicraft import time_shift

df_new = time_shift(variables=["sales", "price"], dataframe=df, id="firm", time="year", shift=1)
```
