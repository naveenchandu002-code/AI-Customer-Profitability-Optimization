import pandas as pd

df = pd.read_csv("outputs/customer_decision_dataset.csv")

VALUE_SCALE = 1000

# Test multiple realistic business assumptions
retention_success_rates = [0.20, 0.30, 0.40]
retention_costs = [50, 100, 150]

results = []

df["Modeled_Economic_Value"] = (
    df["Customer_Value"] * VALUE_SCALE
)

for success_rate in retention_success_rates:
    for cost in retention_costs:

        retention_benefit = (
            df["Churn_Probability"]
            * df["Modeled_Economic_Value"]
            * success_rate
        )

        retention_profit = (
            retention_benefit - cost
        )

        positive_profit = retention_profit.clip(lower=0)

        profitable_customers = (
            retention_profit > 0
        ).sum()

        total_value = positive_profit.sum()

        # $10,000 budget
        budget = 10000
        customers_selected = min(
            int(budget // cost),
            profitable_customers
        )

        ranked = positive_profit.sort_values(
            ascending=False
        )

        selected_profit = ranked.head(
            customers_selected
        )

        optimized_value = selected_profit.sum()
        spend = customers_selected * cost

        roi = (
            optimized_value / spend
            if spend > 0
            else 0
        )

        results.append({
            "Retention_Success_Rate": success_rate,
            "Retention_Cost": cost,
            "Profitable_Customers": profitable_customers,
            "Budget": budget,
            "Customers_Selected": customers_selected,
            "Budget_Spent": spend,
            "Optimized_Value": optimized_value,
            "ROI": roi
        })

results_df = pd.DataFrame(results)

results_df.to_csv(
    "outputs/economic_sensitivity.csv",
    index=False
)

print("Economic sensitivity analysis completed.")
print()

print(
    results_df.round(2).to_string(index=False)
)

print()
print("Best-case scenario:")

best = results_df.loc[
    results_df["Optimized_Value"].idxmax()
]

print(best.round(2).to_string())

print()
print("Conservative scenario:")

conservative = results_df.loc[
    results_df["Optimized_Value"].idxmin()
]

print(conservative.round(2).to_string())