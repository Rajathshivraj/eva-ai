
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

class UploadResponse(BaseModel):
    filename: str
    file_id: str
    message: str
    summary: CSVSummary
