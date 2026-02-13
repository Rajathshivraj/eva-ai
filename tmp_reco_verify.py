
import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import numpy as np
import io
import json

client = TestClient(app)

def test_recommendations():
    np.random.seed(42)
    df = pd.DataFrame({
        'price': np.arange(1, 51, dtype=float).tolist(),           # regression, std > 1 -> normalize
        'cost': (np.arange(1, 51) * 0.9).tolist(),                 # regression, std > 1 -> normalize
        'const_col': [5] * 50,                                     # constant -> drop
        'label': ([0, 1] * 25),                                    # classification
        'category': (['a', 'b', 'c', 'd', 'e'] * 10),             # encode
        'high_card': [f'id_{i}' for i in range(50)],               # high cardinality -> drop
        'mid_miss': [None]*10 + list(range(40)),                    # 20% missing numeric -> impute mean
        'heavy_miss': [None]*45 + [1.0]*5                           # 90% missing -> drop
    })

    csv_content = df.to_csv(index=False).encode('utf-8')
    csv_file = io.BytesIO(csv_content)
    files = {'file': ('reco.csv', csv_file, 'text/csv')}

    try:
        response = client.post("/api/v1/data/upload", files=files)
        if response.status_code != 200:
            print(f"FAILED Status: {response.status_code}")
            print(f"Response: {response.text}")
            return

        suggestions = response.json()['summary']['feature_engineering_suggestions']
        print(json.dumps(suggestions, indent=2))

        # Drop columns should include const_col, high_card, heavy_miss
        assert 'const_col' in suggestions['drop_columns'], "const_col not in drop"
        assert 'high_card' in suggestions['drop_columns'], "high_card not in drop"
        assert 'heavy_miss' in suggestions['drop_columns'], "heavy_miss not in drop"

        # Impute: mid_miss should be mean
        assert suggestions['impute_columns'].get('mid_miss') == 'mean', "mid_miss not imputed as mean"

        # Encode: category should be in encode list
        assert 'category' in suggestions['encode_columns'], "category not in encode"

        # Normalize: price and cost should be normalized (std > 1)
        assert 'price' in suggestions['normalize_columns'], "price not in normalize"
        assert 'cost' in suggestions['normalize_columns'], "cost not in normalize"

        print("test_recommendations PASSED")

    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommendations()
