# SPINEX Symbolic Regression

A Python implementation of symbolic regression from the SPINEX family.

## Installation

```bash
pip install spinex-sr
```

## Quick Start

```python
import pandas as pd
from spinex_sr import SPINEX_SymbolicRegression

# Sample data
data = pd.DataFrame({
    'x1': [1, 2, 3],
    'x2': [4, 5, 6]
})
target = [5, 7, 9]

# Initialize and run
sr = SPINEX_SymbolicRegression(
    data=data,
    target=target,
    actual_function="x1 + x2",
    population_size=50,
    generations=20
)
best_expression = sr.evolve()
print(f"Best expression found: {best_expression}")
```