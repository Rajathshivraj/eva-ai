import pandas as pd
import numpy as np
from typing import Dict, Any, List

def analyze_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform EDA on a DataFrame:
    - Null counts per column
    - Missing percentage per column
    - Numeric summary (mean, std, min, max)
    - Categorical unique counts
    - Correlation matrix (numeric columns)
    - Strong correlations (|corr| >= 0.8, no self-pairs, no duplicates)
    - Target candidates (classification vs regression)
    """
    # Null counts and missing percentage
    null_counts = df.isnull().sum().to_dict()
    total_rows = len(df)
    missing_percent = {col: round((count / total_rows) * 100, 2) for col, count in null_counts.items()}

    # Numeric summary
    numeric_df = df.select_dtypes(include=["number"])
    numeric_summary = {}
    if not numeric_df.empty:
        desc = numeric_df.describe().T
        for col in desc.index:
            numeric_summary[col] = {
                "mean": round(desc.loc[col, "mean"], 4),
                "std": round(desc.loc[col, "std"], 4),
                "min": desc.loc[col, "min"],
                "max": desc.loc[col, "max"]
            }

    # Categorical unique counts
    categorical_df = df.select_dtypes(include=["object", "string", "category"])
    categorical_unique_counts = {}
    if not categorical_df.empty:
        for col in categorical_df.columns:
            categorical_unique_counts[col] = int(categorical_df[col].nunique())

    # Correlation matrix
    correlation_matrix = {}
    strong_correlations: List[Dict[str, Any]] = []
    if not numeric_df.empty and len(numeric_df.columns) > 1:
        corr = numeric_df.corr().fillna(0)
        # Round to 4 decimals and convert to nested dict
        correlation_matrix = {
            col: {row: round(corr.loc[row, col], 4) for row in corr.index}
            for col in corr.columns
        }
        # Strong correlations: |corr| >= 0.8, skip self-pairs and duplicates
        seen = set()
        for i, col_a in enumerate(corr.columns):
            for j, col_b in enumerate(corr.columns):
                if i >= j:
                    continue
                val = corr.loc[col_a, col_b]
                if abs(val) >= 0.8 and (col_a, col_b) not in seen:
                    strong_correlations.append({
                        "feature_1": col_a,
                        "feature_2": col_b,
                        "correlation": round(val, 4)
                    })
                    seen.add((col_a, col_b))

    # Target candidates
    classification_candidates: List[str] = []
    regression_candidates: List[str] = []
    for col in numeric_df.columns:
        nunique = int(numeric_df[col].nunique())
        if nunique <= 1:
            continue  # skip constant columns
        if nunique <= 10:
            classification_candidates.append(col)
        else:
            regression_candidates.append(col)

    target_candidates = {
        "classification_candidates": classification_candidates,
        "regression_candidates": regression_candidates
    }

    return {
        "null_counts": null_counts,
        "missing_percent": missing_percent,
        "numeric_summary": numeric_summary,
        "categorical_unique_counts": categorical_unique_counts,
        "correlation_matrix": correlation_matrix,
        "strong_correlations": strong_correlations,
        "target_candidates": target_candidates
    }
