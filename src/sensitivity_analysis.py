import pandas as pd
import numpy as np

df = pd.read_csv("outputs/customer_decision_dataset.csv")

candidates = df[
    (df["Optimal_Action"] == "RETENTION")
    & (df["Expected_Incremental_Profit"] > 0)
].copy()

candidates = candidates.sort_values(
    "Expected_Incremental_Profit",
    ascending=False
)

COST = 100

budgets = [5000, 10000, 15000, 20000]

results = []

for budget in budgets:

    n = int(budget / COST)

    selected = candidates.head(n)

    optimized_value = selected[
        "Expected_Incremental_Profit"
    ].sum()

    random_values = []

    for seed in range(100):
        random_sample = candidates.sample(
            n=min(n, len(candidates)),
            random_state=seed
        )

        random_values.append(
            random_sample[
                "Expected_Incremental_Profit"
            ].sum()
        )

    random_avg = np.mean(random_values)

    results.append(
        {
            "Budget": budget,
            "Customers_Selected": len(selected),
            "Optimized_Value": optimized_value,
            "Random_Avg_Value": random_avg,
            "Lift_vs_Random": (
                optimized_value - random_avg
            ),
            "Optimized_ROI": (
                optimized_value / budget
            ),
        }
    )

results_df = pd.DataFrame(results)

results_df.to_csv(
    "outputs/sensitivity_analysis.csv",
    index=False
)

print("Sensitivity analysis completed.")
print()
print(results_df.round(2).to_string(index=False))