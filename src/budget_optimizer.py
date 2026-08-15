import pandas as pd

# ==========================================
# 1. Load economics dataset
# ==========================================

df = pd.read_csv(
    "outputs/customer_decision_dataset.csv"
)

# ==========================================
# 2. Budget assumption
# ==========================================

BUDGET = 10000
COST_PER_RETENTION = 100

# ==========================================
# 3. Consider only profitable retention
# ==========================================

candidates = df[
    (df["Optimal_Action"] == "RETENTION")
    & (df["Expected_Incremental_Profit"] > 0)
].copy()

# ==========================================
# 4. Rank customers by expected value
# ==========================================

candidates = candidates.sort_values(
    "Expected_Incremental_Profit",
    ascending=False
)

# ==========================================
# 5. Select customers within budget
# ==========================================

max_customers = int(
    BUDGET / COST_PER_RETENTION
)

selected = candidates.head(max_customers).copy()

selected["Optimization_Action"] = "RETENTION"

# ==========================================
# 6. Calculate budget metrics
# ==========================================

total_spend = (
    len(selected) * COST_PER_RETENTION
)

total_expected_value = (
    selected["Expected_Incremental_Profit"].sum()
)

net_expected_value = (
    total_expected_value
)

roi = (
    net_expected_value / total_spend
    if total_spend > 0
    else 0
)

# ==========================================
# 7. Save optimized customer list
# ==========================================

selected.to_csv(
    "outputs/optimized_customer_targets.csv",
    index=False
)

# ==========================================
# 8. Print results
# ==========================================

print("Budget optimization completed.")
print()

print(f"Available budget: ${BUDGET:,.2f}")
print(f"Customers selected: {len(selected)}")
print(f"Budget spent: ${total_spend:,.2f}")
print(
    f"Expected incremental value: "
    f"${total_expected_value:,.2f}"
)
print(f"Expected ROI: {roi:.2%}")

print()
print("Top 10 selected customers:")

print(
    selected[
        [
            "CLIENTNUM",
            "Churn_Probability",
            "Customer_Value",
            "Expected_Incremental_Profit"
        ]
    ]
    .head(10)
    .to_string(index=False)
)