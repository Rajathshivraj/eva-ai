
import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import numpy as np
import io

client = TestClient(app)

def test_data_quality():
    # Build a CSV that triggers all quality warnings
    df = pd.DataFrame({
        'const_col': [1] * 20,                          # constant column
        'good_num': np.arange(1, 21).tolist(),           # clean numeric
        'high_miss': [None]*15 + [1.0]*5,                # 75% missing
        'cat_hi_card': [f'id_{i}' for i in range(20)],   # 100% unique -> high cardinality
        'cat_normal': ['a', 'b'] * 10                    # normal categorical
    })
    # Add a duplicate row
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    csv_content = df.to_csv(index=False).encode('utf-8')
    csv_file = io.BytesIO(csv_content)
    files = {'file': ('quality.csv', csv_file, 'text/csv')}

    try:
        response = client.post("/api/v1/data/upload", files=files)
        if response.status_code != 200:
            print(f"FAILED Status: {response.status_code}")
            print(f"Response: {response.text}")
            return

        warnings = response.json()['summary']['data_quality_warnings']
        print(f"Warnings: {warnings}")

        assert 'const_col' in warnings['constant_columns'], "const_col not detected"
        assert 'high_miss' in warnings['high_missing_columns'], "high_miss not detected"
        assert 'cat_hi_card' in warnings['high_cardinality_columns'], "cat_hi_card not detected"
        assert warnings['duplicate_row_count'] >= 1, "duplicate not detected"

        print("test_data_quality PASSED")

    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_quality()
