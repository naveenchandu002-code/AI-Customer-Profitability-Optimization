import pandas as pd

# ==========================================
# 1. Load decision dataset
# ==========================================

df = pd.read_csv("outputs/customer_decision_dataset.csv")


# ==========================================
# 2. Scenario assumptions
# ==========================================
# These are analytical assumptions, NOT actual
# bank financial data.

VALUE_SCALE = 1000

RETENTION_SUCCESS_RATE = 0.30
UPSELL_CONVERSION_RATE = 0.20
CROSS_SELL_CONVERSION_RATE = 0.15
ENGAGEMENT_CONVERSION_RATE = 0.10

UPSELL_VALUE_LIFT = 0.25
CROSS_SELL_VALUE_LIFT = 0.20
ENGAGEMENT_VALUE_LIFT = 0.05

RETENTION_COST = 100
UPSELL_COST = 75
CROSS_SELL_COST = 50
ENGAGEMENT_COST = 20


# ==========================================
# 3. Modeled economic value
# ==========================================

df["Modeled_Economic_Value"] = (
    df["Customer_Value"] * VALUE_SCALE
)


# ==========================================
# 4. Expected incremental value by action
# ==========================================

# RETENTION
# Value preserved if a customer who is likely
# to churn is successfully retained.

df["Retention_Benefit"] = (
    df["Churn_Probability"]
    * df["Modeled_Economic_Value"]
    * RETENTION_SUCCESS_RATE
)

df["Retention_Profit"] = (
    df["Retention_Benefit"]
    - RETENTION_COST
)


# UPSELL
# Assumed incremental value generated from
# successful upsell.

df["Upsell_Benefit"] = (
    df["Modeled_Economic_Value"]
    * UPSELL_CONVERSION_RATE
    * UPSELL_VALUE_LIFT
)

df["Upsell_Profit"] = (
    df["Upsell_Benefit"]
    - UPSELL_COST
)


# CROSS-SELL

df["CrossSell_Benefit"] = (
    df["Modeled_Economic_Value"]
    * CROSS_SELL_CONVERSION_RATE
    * CROSS_SELL_VALUE_LIFT
)

df["CrossSell_Profit"] = (
    df["CrossSell_Benefit"]
    - CROSS_SELL_COST
)


# ENGAGEMENT

df["Engagement_Benefit"] = (
    df["Modeled_Economic_Value"]
    * ENGAGEMENT_CONVERSION_RATE
    * ENGAGEMENT_VALUE_LIFT
)

df["Engagement_Profit"] = (
    df["Engagement_Benefit"]
    - ENGAGEMENT_COST
)


# ==========================================
# 5. Select economically best action
# ==========================================

profit_columns = {
    "RETENTION": "Retention_Profit",
    "UPSELL": "Upsell_Profit",
    "CROSS_SELL": "CrossSell_Profit",
    "ENGAGE": "Engagement_Profit",
}

profit_matrix = pd.DataFrame(
    {
        action: df[column]
        for action, column in profit_columns.items()
    }
)

df["Optimal_Action"] = profit_matrix.idxmax(axis=1)

df["Expected_Incremental_Profit"] = (
    profit_matrix.max(axis=1)
)

# Do not recommend an intervention if every
# available action has negative expected profit.

df.loc[
    df["Expected_Incremental_Profit"] <= 0,
    "Optimal_Action"
] = "DO NOTHING"

df.loc[
    df["Expected_Incremental_Profit"] <= 0,
    "Expected_Incremental_Profit"
] = 0


# ==========================================
# 6. Cost of selected action
# ==========================================

cost_map = {
    "RETENTION": RETENTION_COST,
    "UPSELL": UPSELL_COST,
    "CROSS_SELL": CROSS_SELL_COST,
    "ENGAGE": ENGAGEMENT_COST,
    "DO NOTHING": 0,
}

df["Intervention_Cost"] = (
    df["Optimal_Action"].map(cost_map)
)


# ==========================================
# 7. ROI
# ==========================================

df["Expected_ROI"] = 0.0

mask = df["Intervention_Cost"] > 0

df.loc[mask, "Expected_ROI"] = (
    df.loc[mask, "Expected_Incremental_Profit"]
    / df.loc[mask, "Intervention_Cost"]
)


# ==========================================
# 8. Save results
# ==========================================

df.to_csv(
    "outputs/customer_decision_dataset.csv",
    index=False
)


# ==========================================
# 9. Summary
# ==========================================

print("Action economics engine completed.")
print()

print("Optimal actions:")
print(
    df["Optimal_Action"]
    .value_counts()
)

print()

print("Total expected incremental value:")
print(
    round(
        df["Expected_Incremental_Profit"].sum(),
        2
    )
)

print()

print("Customers receiving an intervention:")
print(
    int(
        (df["Optimal_Action"] != "DO NOTHING").sum()
    )
)

print()

print("Action economics summary:")

summary = (
    df.groupby("Optimal_Action")
    .agg(
        Customers=("CLIENTNUM", "count"),
        Total_Expected_Value=(
            "Expected_Incremental_Profit",
            "sum"
        ),
        Avg_Expected_Value=(
            "Expected_Incremental_Profit",
            "mean"
        ),
        Avg_Cost=(
            "Intervention_Cost",
            "mean"
        ),
        Avg_ROI=(
            "Expected_ROI",
            "mean"
        ),
    )
    .sort_values(
        "Total_Expected_Value",
        ascending=False
    )
)

print(
    summary.round(2)
)