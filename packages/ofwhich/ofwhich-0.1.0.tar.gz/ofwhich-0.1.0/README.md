# ofwhich

Easy drill-down into dataset for high-level summary.

## In this README :point_down:

- [Usage](#usage)
  - [Installation](#installation)
  - [Getting started](#getting-started)
- [Contributing](#contributing)

## Usage

### Installation

Make sure you are in the right environment and install the package
```
pip install ofwhich
```

### Getting started

1. Have a dataframe to run insights from. Example:
```python
import pandas as pd
import numpy as np

num_rows = 100

df = pd.DataFrame({
    'Category': np.random.choice(['X', 'Y', 'Z'], size=num_rows),
    'Bool': np.random.choice([True, False], size=num_rows)
})

df.head()
```
```
  Category  Bool
0        Z  True
1        X  False
2        Y  False
...
```

2. Use ofwhich:

```python
from ofwhich import OfWhich
_ = OfWhich(df, 'Category1', 'Bool1')
```
3. Enjoy the output :)
```
Total 100 records
    Of which X 37 records
        Of which True 19 records
        Of which False 18 records
    Of which Y 35 records
        Of which True 19 records
        Of which False 16 records
    Of which Z 28 records
        Of which True 16 records
        Of which False 12 records
```

## Contributing

If you find a bug, please open an issue.
Ideas for new features and improvement are welcome! Feel free to open an issue or PR.
