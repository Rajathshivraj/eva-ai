
import pandas as pd
from typing import Dict, Any

def analyze_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform basic EDA on a DataFrame:
    - Null counts per column
    - Missing percentage per column
    - Numeric summary (mean, std, min, max)
    - Categorical unique counts
    """
    # Null counts and missing percentage
    null_counts = df.isnull().sum().to_dict()
    total_rows = len(df)
    missing_percent = {col: round((count / total_rows) * 100, 2) for col, count in null_counts.items()}

    # Numeric summary
    numeric_df = df.select_dtypes(include=['number'])
    numeric_summary = {}
    if not numeric_df.empty:
        # describe() returns a DataFrame, we transact it to dict
        desc = numeric_df.describe().T
        for col in desc.index:
            numeric_summary[col] = {
                "mean": round(desc.loc[col, "mean"], 4),
                "std": round(desc.loc[col, "std"], 4),
                "min": desc.loc[col, "min"],
                "max": desc.loc[col, "max"]
            }

    # Categorical unique counts
    categorical_df = df.select_dtypes(include=['object', 'string', 'category'])
    categorical_unique_counts = {}
    if not categorical_df.empty:
        for col in categorical_df.columns:
            categorical_unique_counts[col] = int(categorical_df[col].nunique())

    return {
        "null_counts": null_counts,
        "missing_percent": missing_percent,
        "numeric_summary": numeric_summary,
        "categorical_unique_counts": categorical_unique_counts
    }
