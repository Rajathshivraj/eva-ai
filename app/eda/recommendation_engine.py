import pandas as pd
from typing import Dict, Any, List, Optional

def generate_recommendations(
    df: pd.DataFrame,
    missing_percent: Dict[str, float],
    categorical_unique_counts: Dict[str, int],
    numeric_summary: Dict[str, Dict[str, float]],
    data_quality_warnings: Dict[str, Any],
    target_candidates: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Generate rule-based feature engineering recommendations.
    """
    constant_columns = data_quality_warnings.get("constant_columns", [])
    high_cardinality_columns = data_quality_warnings.get("high_cardinality_columns", [])

    # Drop columns: constant, >80% missing, high cardinality
    drop_columns = list(set(
        constant_columns
        + [col for col, pct in missing_percent.items() if pct > 80]
        + high_cardinality_columns
    ))

    # Impute columns: 10 < missing_percent <= 80
    numeric_cols = set(df.select_dtypes(include=["number"]).columns)
    categorical_cols = set(df.select_dtypes(include=["object", "string", "category"]).columns)

    impute_columns: Dict[str, str] = {}
    for col, pct in missing_percent.items():
        if 10 < pct <= 80:
            if col in numeric_cols:
                impute_columns[col] = "mean"
            elif col in categorical_cols:
                impute_columns[col] = "mode"

    # Encode columns: categorical columns not in high cardinality
    encode_columns = [
        col for col in categorical_cols
        if col not in high_cardinality_columns
    ]

    # Normalize columns: numeric columns where std > 1
    normalize_columns = [
        col for col, stats in numeric_summary.items()
        if stats.get("std", 0) > 1
    ]

    # Potential target
    regression = target_candidates.get("regression_candidates", [])
    classification = target_candidates.get("classification_candidates", [])

    potential_target: Optional[str] = None
    if len(regression) == 1:
        potential_target = regression[0]
    elif len(classification) == 1:
        potential_target = classification[0]

    return {
        "drop_columns": drop_columns,
        "impute_columns": impute_columns,
        "encode_columns": encode_columns,
        "normalize_columns": normalize_columns,
        "potential_target": potential_target
    }
