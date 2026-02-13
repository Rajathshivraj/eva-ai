
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

def test_extended_eda():
    # Use enough rows so price has >10 unique values for regression candidate
    np.random.seed(42)
    df = pd.DataFrame({
        'price': np.arange(1, 51).tolist(),               # 50 unique -> regression
        'cost': (np.arange(1, 51) * 0.9).tolist(),         # correlated with price
        'label': ([0, 1] * 25),                            # 2 unique -> classification
        'category': (['a', 'b', 'c', 'd', 'e'] * 10)
    })
    csv_content = df.to_csv(index=False).encode('utf-8')
    csv_file = io.BytesIO(csv_content)

    files = {'file': ('extended.csv', csv_file, 'text/csv')}

    try:
        response = client.post("/api/v1/data/upload", files=files)

        if response.status_code != 200:
            print(f"FAILED Status: {response.status_code}")
            print(f"Response: {response.text}")
            return

        summary = response.json()['summary']

        # Correlation matrix
        assert 'correlation_matrix' in summary, "Missing correlation_matrix"
        assert 'price' in summary['correlation_matrix'], "Missing price in corr matrix"
        assert 'cost' in summary['correlation_matrix']['price'], "Missing cost in price corr"

        # Strong correlations should include price-cost pair
        assert len(summary['strong_correlations']) > 0, "No strong correlations found"
        pair = summary['strong_correlations'][0]
        assert pair['feature_1'] == 'price' and pair['feature_2'] == 'cost', "Wrong strong pair"
        assert abs(pair['correlation']) >= 0.8, "Correlation too low"

        # Target candidates
        assert 'label' in summary['target_candidates']['classification_candidates'], "label not classification"
        assert 'price' in summary['target_candidates']['regression_candidates'], "price not regression"
        assert 'cost' in summary['target_candidates']['regression_candidates'], "cost not regression"

        print("test_extended_eda PASSED")

    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extended_eda()
