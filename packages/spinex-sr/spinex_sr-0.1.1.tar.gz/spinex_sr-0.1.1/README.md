# SPINEX Symbolic Regression

A Python implementation of symbolic regression from the SPINEX family.

## Installation

```bash
pip install spinex-sr
```

## Quick Start

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spinex_sr import SPINEX_SymbolicRegression

if __name__ == "__main__":
    # Generate sample data for the multi-variable problem
    np.random.seed(42)
    X = np.linspace(0, 10, 100)
    Y = np.linspace(5, 15, 100)
    Z = np.linspace(5, 15, 100)
    # Define the actual function with multiple variables
    def actual_function_multi(X, Z):
        return X + Y + 3 * Z
    y_multi = actual_function_multi(X, Z)
    df_multi = pd.DataFrame({'X': X, 'Y': Y, 'Z': Z})
    # Create an instance of Symbolic_SPINEX for the multi-variable problem
    symbolic_spinex_multi = SPINEX_SymbolicRegression(
        df_multi, y_multi,
        actual_function="y = 2 * X**2 + 3 * X + 5",
        max_depth=3,
        population_size=25,
        generations=55,
        explainability_level='none',
        plot_results=True,
        early_stopping_metric='r2',
        early_stopping_value=0.79,
        patience=3,
        n_jobs=-1,
        last_resort=True,  # Enable last resort mode
        force_all_variables=False
    )
    symbolic_spinex_multi.initialize_population()
    best_expression_multi = symbolic_spinex_multi.evolve()
    symbolic_spinex_multi.best_expression = best_expression_multi
    # Call explain() to get the advanced explanation and plot for multi-variable
    symbolic_spinex_multi.explain()

    # Generate sample data for the single-variable problem
    X_single = np.linspace(0, 10, 100)
    # Define the actual function for the single-variable problem
    def actual_function_single(X):
        return 2 * X**2 + 3 * X + 5
    y_single = actual_function_single(X_single)
    df_single = pd.DataFrame({'X': X_single})
    # Create an instance of Symbolic_SPINEX for the single-variable problem
    symbolic_spinex_single = SPINEX_SymbolicRegression(
        df_single, y_single,
        actual_function="y = 2 * X**2 + 3 * X + 5",
        max_depth=3,
        population_size=50,
        generations=50,
        explainability_level='advanced',
        plot_results=True,
        early_stopping_metric='mse',
        early_stopping_value=200,
        patience=3,
        n_jobs=-1,
        dynamic_elite=True,
        last_resort=True,  # Enable last resort mode
        force_all_variables=True
    )
    symbolic_spinex_single.initialize_population()
    best_expression_single = symbolic_spinex_single.evolve()
    symbolic_spinex_single.best_expression = best_expression_single
    # Call explain() to get the advanced explanation and plot for single-variable
    symbolic_spinex_single.explain()

    plt.show()
```