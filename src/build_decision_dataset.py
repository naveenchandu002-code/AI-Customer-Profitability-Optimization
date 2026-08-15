import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# 1. Load data
# -----------------------------
df = pd.read_csv("data/processed_customers.csv")

# -----------------------------
# 2. Prepare ML data
# -----------------------------
X = df.drop(columns=["Attrition_Flag", "CLIENTNUM"])
y = df["Attrition_Flag"].eq("Attrited Customer").astype(int)

categorical = X.select_dtypes(include="str").columns
numerical = X.select_dtypes(exclude="str").columns

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", StandardScaler(), numerical),
    ]
)

# -----------------------------
# 3. Train churn model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42,
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            XGBClassifier(
                n_estimators=300,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                eval_metric="logloss",
                random_state=42,
            ),
        ),
    ]
)

model.fit(X_train, y_train)

# -----------------------------
# 4. Generate churn probability
# -----------------------------
df["Churn_Probability"] = model.predict_proba(X)[:, 1]

# -----------------------------
# 5. Calculate modeled customer value
# -----------------------------
value_scaler = MinMaxScaler()

df[["Txn_Value_Score", "Revolving_Value_Score"]] = value_scaler.fit_transform(
    df[["Total_Trans_Amt", "Total_Revolving_Bal"]]
)

df["Customer_Value"] = (
    0.6 * df["Txn_Value_Score"]
    + 0.4 * df["Revolving_Value_Score"]
)

# -----------------------------
# 6. Save decision dataset
# -----------------------------
output_columns = [
    "CLIENTNUM",
    "Attrition_Flag",
    "Churn_Probability",
    "Customer_Value",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Total_Revolving_Bal",
    "Credit_Limit",
    "Avg_Utilization_Ratio",
    "Months_Inactive_12_mon",
]

decision_df = df[output_columns].copy()

decision_df.to_csv(
    "outputs/customer_decision_dataset.csv",
    index=False,
)

print("Decision dataset created successfully.")
print(f"Customers: {len(decision_df)}")
print(f"Saved to: outputs/customer_decision_dataset.csv")
print()
print(decision_df.head(10).to_string(index=False))