
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.common import UploadResponse, CSVSummary
from app.services.data_service import process_csv
from app.core.config import settings
import shutil
import os
import uuid

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a CSV dataset, validate it, and return metadata.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    # Process and validate CSV logic
    csv_meta = await process_csv(file)
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    try:
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
    # Explicitly validate summary
    summary = CSVSummary(**csv_meta)
        
    return UploadResponse(
        filename=file.filename,
        file_id=file_id,
        message="File uploaded and validated successfully",
        summary=summary
    )
