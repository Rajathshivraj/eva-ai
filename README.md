
# EVA - Exploratory Visualization & AutoML Assistant

EVA is a locally-running AI data science assistant designed to automate EDA, generate visualizations, suggest feature engineering, and build baseline ML models.

## Features

- **Data Ingestion**: Support for CSV uploads.
- **Automated EDA**: Statistical summaries and visualizations.
- **ML Pipeline**: Automated training using Scikit-learn and XGBoost with Optuna tuning.
- **Local LLM Integration**: Privacy-first analysis using local models.
- **Notebook Export**: Generates reproducible Jupyter Notebooks.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/eva.git
   cd eva
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker

1. **Build the image**:
   ```bash
   docker build -t eva-app .
   ```

2. **Run container**:
   ```bash
   docker run -p 8000:8000 -v $(pwd)/data:/app/data eva-app
   ```

## API Documentation

Once running, access the API docs at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc
