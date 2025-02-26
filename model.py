import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd

def train_model():
    mlflow.set_tracking_uri("/mlflow_data")
    mlflow.set_experiment("docker_iris_classification")

    # Load dataset
    data = load_iris()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='target')

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Start MLflow run
    with mlflow.start_run():
        # Training
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)

        # Logging parameters and metrics
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
        mlflow.log_metric("precision", precision_score(y_test, y_pred, average='macro'))
        mlflow.log_metric("recall", recall_score(y_test, y_pred, average='macro'))
        mlflow.log_metric("f1_score", f1_score(y_test, y_pred, average='macro'))

        # Log model
        mlflow.sklearn.log_model(model, "random_forest_model")

        print("Model training completed and logged to MLflow.")

if __name__ == "__main__":
    train_model()
