
import pandas as pd
from fastapi import UploadFile, HTTPException
import io

async def process_csv(file: UploadFile) -> dict:
    """
    Read a CSV file, validate it, and return metadata.
    """
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        # Reset file pointer for subsequent saving if needed
        await file.seek(0)
        
        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": df.columns.tolist(),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Unable to parse the CSV file. Please check the format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")
