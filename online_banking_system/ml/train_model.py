import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from joblib import dump


def train_loan_model(csv_path="../loan_amount_prediction_dataset_v2.csv",
                     save_path="./loan_amount_model.joblib"):
    """Train the ML model using the provided dataset."""

    # Load CSV
    df = pd.read_csv(csv_path)

    # Expected columns:
    # 1. age
    # 2. monthly_income
    # 3. credit_score
    # 4. loan_tenure_years
    # 5. existing_loan_amount
    # 6. dependents
    # 7. loan_amount (target)

    feature_cols = [
        "Age",
        "Monthly_Income",
        "Credit_Score",
        "Loan_Tenure_Years",
        "Existing_Loan_Amount",
        "Num_of_Dependents"
    ]

    target_col = "Loan_Amount"

    # X = Inputs
    X = df[feature_cols]

    # y = Label / Target
    y = df[target_col]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Pipeline: Scaling + Model
    numeric_features = feature_cols

    numeric_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features)
        ]
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", model)
    ])

    # Train model
    pipeline.fit(X_train, y_train)

    # Evaluate
    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("Model Training Completed")
    print(f"MAE: {mae:.2f}")
    print(f"R² Score: {r2:.3f}")

    # Save model
    dump(pipeline, save_path)
    print(f"Model saved to: {save_path}")


if __name__ == "__main__":
    train_loan_model()
