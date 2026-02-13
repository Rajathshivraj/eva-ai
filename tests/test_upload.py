
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
    
    response = client.post("/api/v1/data/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data['filename'] == 'test.csv'
    assert 'file_id' in data
    assert data['message'] == "File uploaded and validated successfully"
    assert data['summary']['rows'] == 3
    assert data['summary']['columns'] == 2
    assert data['summary']['column_names'] == ['A', 'B']
    
    # Verify EDA stats
    assert data['summary']['null_counts']['A'] == 0
    assert data['summary']['missing_percent']['A'] == 0.0
    assert data['summary']['numeric_summary']['A']['min'] == 1.0
    assert data['summary']['numeric_summary']['A']['max'] == 3.0
    assert data['summary']['categorical_unique_counts']['B'] == 3

def test_upload_invalid_extension():
    files = {'file': ('test.txt', io.BytesIO(b"some text"), 'text/plain')}
    response = client.post("/api/v1/data/upload", files=files)
    assert response.status_code == 400
    assert "Only CSV files are allowed" in response.json()['detail']
