import pandas as pd

# Load decision dataset
df = pd.read_csv("outputs/customer_decision_dataset.csv")

# -----------------------------
# Decision thresholds
# -----------------------------
HIGH_CHURN = 0.70
HIGH_VALUE = 0.60
MEDIUM_VALUE = 0.30
HIGH_ENGAGEMENT = 70

# -----------------------------
# Assign recommended action
# -----------------------------
def recommend_action(row):

    churn = row["Churn_Probability"]
    value = row["Customer_Value"]
    transactions = row["Total_Trans_Ct"]

    # High-value customers at serious churn risk
    if churn >= HIGH_CHURN and value >= HIGH_VALUE:
        return "RETENTION"

    # Valuable customers with low churn risk and strong engagement
    elif churn < 0.30 and value >= HIGH_VALUE and transactions >= HIGH_ENGAGEMENT:
        return "UPSELL"

    # Engaged customers with growth potential
    elif churn < 0.30 and transactions >= HIGH_ENGAGEMENT:
        return "CROSS_SELL"

    # High-risk but economically unattractive customers
    elif churn >= HIGH_CHURN and value < MEDIUM_VALUE:
        return "DO NOTHING"

    # Remaining customers
    else:
        return "ENGAGE"


df["Recommended_Action"] = df.apply(recommend_action, axis=1)

# -----------------------------
# Save results
# -----------------------------
df.to_csv(
    "outputs/customer_decision_dataset.csv",
    index=False
)

# -----------------------------
# Summary
# -----------------------------
print("Decision engine completed.")
print()
print("Recommended actions:")
print(df["Recommended_Action"].value_counts())
print()

print("Average customer value by action:")
print(
    df.groupby("Recommended_Action")["Customer_Value"]
    .mean()
    .sort_values(ascending=False)
    .round(3)
)

print()
print("Average churn probability by action:")
print(
    df.groupby("Recommended_Action")["Churn_Probability"]
    .mean()
    .sort_values(ascending=False)
    .round(3)
)