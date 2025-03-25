# MLScore

A comprehensive machine learning evaluation metrics library that provides a simple interface to calculate multiple evaluation metrics at once.

## Installation

```bash
pip install mlscore
```

## Usage

### Basic Usage

```python
from mlscore import score, score_c, score_r
import numpy as np

# Example 1: Classification
y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
y_pred = np.array([0, 1, 0, 0, 0, 1, 0, 1, 0, 1])

# Using score_c for classification (automatically prints results)
score_c(y_true, y_pred)

# Example 2: Regression
y_true_reg = np.array([1.2, 2.3, 3.4, 4.5])
y_pred_reg = np.array([1.1, 2.4, 3.3, 4.6])

# Using score_r for regression (automatically prints results)
score_r(y_true_reg, y_pred_reg)

# Example 3: Automatic detection
score(y_true, y_pred)  # Will automatically detect and print results
```

### Getting Metrics Without Printing

```python
# Get metrics dictionary without printing
metrics = score_c(y_true, y_pred, print_results=False)

# Access specific metrics
print(metrics['Accuracy'])
print(metrics['Precision'])
print(metrics['F1 Score'])
```

### Available Functions

1. `score(y_true, y_pred, print_results=True)`
   - Automatically detects if the problem is classification or regression
   - Prints results by default
   - Returns a dictionary of metrics

2. `score_c(y_true, y_pred, print_results=True)`
   - Specifically for classification problems
   - Prints results by default
   - Returns a dictionary of classification metrics

3. `score_r(y_true, y_pred, print_results=True)`
   - Specifically for regression problems
   - Prints results by default
   - Returns a dictionary of regression metrics

## Available Metrics

### Classification Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score (for binary classification)
- Confusion Matrix

### Regression Metrics
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- R² Score
- Adjusted R² Score

## Output Format

The library provides two ways to access the metrics:

1. **Printed Output** (default):
```
==================================================
Problem Type: Classification
==================================================
Accuracy: 0.9000
Precision: 0.9167
Recall: 0.9000
F1 Score: 0.8990
ROC-AUC: 0.9000

Confusion Matrix:
  [5, 0]
  [1, 4]
```

2. **Dictionary Output**:
```python
{
    'Accuracy': 0.9,
    'Precision': 0.9167,
    'Recall': 0.9,
    'F1 Score': 0.8990,
    'ROC-AUC': 0.9,
    'Confusion Matrix': [[5, 0], [1, 4]],
    'Problem Type': 'Classification'
}
```

## Requirements

- Python >= 3.6
- NumPy >= 1.19.0
- scikit-learn >= 0.24.0

## License

MIT License 