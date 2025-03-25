import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from typing import Union, List, Dict, Any

def _is_classification(y_true: np.ndarray, y_pred: np.ndarray) -> bool:
    """Determine if the problem is classification or regression."""
    unique_values = np.unique(np.concatenate([y_true, y_pred]))
    return len(unique_values) <= 10 and all(isinstance(x, (int, np.integer)) for x in unique_values)

def _calculate_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate classification metrics."""
    metrics = {}
    
    try:
        metrics["Accuracy"] = accuracy_score(y_true, y_pred)
        metrics["Precision"] = precision_score(y_true, y_pred, average='weighted')
        metrics["Recall"] = recall_score(y_true, y_pred, average='weighted')
        metrics["F1 Score"] = f1_score(y_true, y_pred, average='weighted')
        
        # ROC-AUC requires probability scores, so we'll skip it if not available
        if len(np.unique(y_true)) == 2:  # Binary classification
            try:
                metrics["ROC-AUC"] = roc_auc_score(y_true, y_pred)
            except:
                pass
        
        # Add confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics["Confusion Matrix"] = cm.tolist()
        
    except Exception as e:
        print(f"Warning: Some classification metrics could not be calculated: {str(e)}")
    
    return metrics

def _calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate regression metrics."""
    metrics = {}
    
    try:
        metrics["MSE"] = mean_squared_error(y_true, y_pred)
        metrics["RMSE"] = np.sqrt(metrics["MSE"])
        metrics["MAE"] = mean_absolute_error(y_true, y_pred)
        metrics["R² Score"] = r2_score(y_true, y_pred)
        
        # Calculate Adjusted R²
        n = len(y_true)
        p = 1  # number of predictors (assuming single variable for now)
        adjusted_r2 = 1 - (1 - metrics["R² Score"]) * (n - 1) / (n - p - 1)
        metrics["Adjusted R²"] = adjusted_r2
        
    except Exception as e:
        print(f"Warning: Some regression metrics could not be calculated: {str(e)}")
    
    return metrics

def _print_metrics(metrics: Dict[str, Any]) -> None:
    """Print metrics in a formatted way"""
    print("\n" + "="*50)
    print(f"Problem Type: {metrics['Problem Type']}")
    print("="*50)
    
    for metric_name, value in metrics.items():
        if metric_name != "Problem Type":
            if metric_name == "Confusion Matrix":
                print(f"\n{metric_name}:")
                for row in value:
                    print(f"  {row}")
            else:
                print(f"{metric_name}: {value:.4f}")

def score(y_true: Union[List, np.ndarray], y_pred: Union[List, np.ndarray], print_results: bool = True) -> Dict[str, Any]:
    """
    Calculate various machine learning evaluation metrics based on true and predicted values.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        print_results: Whether to print the results directly
        
    Returns:
        Dictionary containing various evaluation metrics
    """
    # Convert inputs to numpy arrays
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Determine if classification or regression
    is_classification = _is_classification(y_true, y_pred)
    
    # Calculate metrics based on problem type
    if is_classification:
        metrics = _calculate_classification_metrics(y_true, y_pred)
        metrics["Problem Type"] = "Classification"
    else:
        metrics = _calculate_regression_metrics(y_true, y_pred)
        metrics["Problem Type"] = "Regression"
    
    if print_results:
        _print_metrics(metrics)
    
    return metrics

def score_c(y_true: Union[List, np.ndarray], y_pred: Union[List, np.ndarray], print_results: bool = True) -> Dict[str, Any]:
    """
    Calculate classification metrics specifically.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        print_results: Whether to print the results directly
        
    Returns:
        Dictionary containing classification metrics
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    metrics = _calculate_classification_metrics(y_true, y_pred)
    metrics["Problem Type"] = "Classification"
    
    if print_results:
        _print_metrics(metrics)
    
    return metrics

def score_r(y_true: Union[List, np.ndarray], y_pred: Union[List, np.ndarray], print_results: bool = True) -> Dict[str, Any]:
    """
    Calculate regression metrics specifically.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        print_results: Whether to print the results directly
        
    Returns:
        Dictionary containing regression metrics
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    metrics = _calculate_regression_metrics(y_true, y_pred)
    metrics["Problem Type"] = "Regression"
    
    if print_results:
        _print_metrics(metrics)
    
    return metrics 