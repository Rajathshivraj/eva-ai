
import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import io

client = TestClient(app)

def test_upload_csv():
    # Create a dummy CSV
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['x', 'y', 'z']
    })
    csv_content = df.to_csv(index=False).encode('utf-8')
    csv_file = io.BytesIO(csv_content)
    
    files = {'file': ('test.csv', csv_file, 'text/csv')}
    
    try:
        response = client.post("/api/v1/data/upload", files=files)
        
        if response.status_code != 200:
            print(f"FAILED test_upload_csv Status: {response.status_code}")
            print(f"Response: {response.text}")
            return
            
        data = response.json()
        
        # Basic Validation
        assert data['filename'] == 'test.csv', "Filename mismatch"
        assert 'file_id' in data, "Missing file_id"
        assert data['summary']['rows'] == 3, "Row count mismatch"
        
        # EDA Validation
        summary = data['summary']
        print(f"EDA Summary Received: {summary}")
        
        assert summary['null_counts']['A'] == 0, "Null count check failed"
        assert summary['missing_percent']['A'] == 0.0, "Missing percent check failed"
        assert summary['numeric_summary']['A']['min'] == 1.0, "Min value check failed"
        assert summary['numeric_summary']['A']['max'] == 3.0, "Max value check failed"
        assert summary['categorical_unique_counts']['B'] == 3, "Unique count check failed"
        
        print("test_upload_csv PASSED")
        
    except Exception as e:
        print(f"FAILED validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_upload_csv()
