import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

# ==========================================
# 1. Load data
# ==========================================

df = pd.read_csv("data/processed_customers.csv")

X = df.drop(columns=["Attrition_Flag", "CLIENTNUM"])
y = df["Attrition_Flag"].eq("Attrited Customer").astype(int)

# ==========================================
# 2. Prepare columns
# ==========================================

categorical = X.select_dtypes(include="str").columns
numerical = X.select_dtypes(exclude="str").columns

# ==========================================
# 3. Out-of-fold predictions
# ==========================================

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

oof_probability = pd.Series(
    index=df.index,
    dtype=float
)

for fold, (train_idx, valid_idx) in enumerate(
    skf.split(X, y), start=1
):

    X_train = X.iloc[train_idx]
    X_valid = X.iloc[valid_idx]

    y_train = y.iloc[train_idx]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical,
            ),
            (
                "num",
                StandardScaler(),
                numerical,
            ),
        ]
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

    oof_probability.iloc[valid_idx] = (
        model.predict_proba(X_valid)[:, 1]
    )

    print(f"Completed fold {fold}/5")


# ==========================================
# 4. Store OOF churn probability
# ==========================================

df["Churn_Probability"] = oof_probability


# ==========================================
# 5. Customer value score
# ==========================================

value_scaler = MinMaxScaler()

df[
    ["Txn_Value_Score", "Revolving_Value_Score"]
] = value_scaler.fit_transform(
    df[
        [
            "Total_Trans_Amt",
            "Total_Revolving_Bal",
        ]
    ]
)

df["Customer_Value"] = (
    0.6 * df["Txn_Value_Score"]
    + 0.4 * df["Revolving_Value_Score"]
)


# ==========================================
# 6. Save OOF decision dataset
# ==========================================

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
    index=False
)


# ==========================================
# 7. Validation summary
# ==========================================

print()
print("OOF decision dataset created successfully.")
print(f"Customers: {len(decision_df)}")
print(
    f"Missing probabilities: "
    f"{decision_df['Churn_Probability'].isna().sum()}"
)

print()
print(
    decision_df["Churn_Probability"]
    .describe()
    .round(4)
)