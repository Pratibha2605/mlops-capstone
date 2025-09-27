import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------
# Load dataset
# -------------------------------
data = pd.read_csv("data/housing.csv")  # adjust path if needed

# Features and target
X = data[["area"]]   # feature column
y = data["price"]    # target column

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# MLflow configuration
# -------------------------------
mlflow.set_tracking_uri("http://127.0.0.1:5000")  # MLflow server
mlflow.set_experiment("mlops-capstone")

# Enable MLflow autologging
mlflow.autolog()

# -------------------------------
# Train and log model
# -------------------------------
with mlflow.start_run(run_name="linear_regression"):
    # Define and train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Log params and metrics manually (optional, autolog also handles this)
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2", r2)

    # Log model to MLflow
    mlflow.sklearn.log_model(model, artifact_path="linear_regression_model")

    # Save locally for FastAPI
    joblib.dump(model, "model.pkl")

    print("Model trained, logged to MLflow, and saved locally as model.pkl.")
    print(f"MSE: {mse}")
    print(f"R2: {r2}")


#mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000
# mlflow-artifacts:/438705199425615622/models/m-1a7cf8ede25a4b0fb35c94ca3e90648f/artifacts/MLmodel