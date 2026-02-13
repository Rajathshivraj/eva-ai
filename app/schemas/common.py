
from pydantic import BaseModel
from typing import List, Dict, Any

class HealthCheck(BaseModel):
    status: str
    version: str

class CSVSummary(BaseModel):
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]
    null_counts: Dict[str, int]
    missing_percent: Dict[str, float]
    numeric_summary: Dict[str, Dict[str, float]]
    categorical_unique_counts: Dict[str, int]
    correlation_matrix: Dict[str, Dict[str, float]]
    strong_correlations: List[Dict[str, Any]]
    target_candidates: Dict[str, List[str]]

class UploadResponse(BaseModel):
    filename: str
    file_id: str
    message: str
    summary: CSVSummary
