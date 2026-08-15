import pandas as pd

# Load final decision dataset
df = pd.read_csv("outputs/customer_decision_dataset.csv")

# Select only fields needed for the executive dashboard
dashboard_columns = [
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
    "Recommended_Action",
    "Optimal_Action",
    "Expected_Incremental_Profit",
    "Intervention_Cost",
    "Expected_ROI",
]

dashboard_df = df[dashboard_columns].copy()

# Create business-friendly categories
dashboard_df["Churn_Risk"] = pd.cut(
    dashboard_df["Churn_Probability"],
    bins=[-0.01, 0.30, 0.70, 1.00],
    labels=["Low", "Medium", "High"]
)

dashboard_df["Customer_Value_Tier"] = pd.cut(
    dashboard_df["Customer_Value"],
    bins=[-0.01, 0.30, 0.60, 1.00],
    labels=["Low", "Medium", "High"]
)

# Round model outputs for dashboard readability
dashboard_df["Churn_Probability"] = (
    dashboard_df["Churn_Probability"].round(4)
)

dashboard_df["Customer_Value"] = (
    dashboard_df["Customer_Value"].round(4)
)

dashboard_df["Expected_Incremental_Profit"] = (
    dashboard_df["Expected_Incremental_Profit"].round(2)
)

dashboard_df["Intervention_Cost"] = (
    dashboard_df["Intervention_Cost"].round(2)
)

dashboard_df["Expected_ROI"] = (
    dashboard_df["Expected_ROI"].round(4)
)

# Save Power BI-ready dataset
dashboard_df.to_csv(
    "dashboard/customer_profitability_dashboard.csv",
    index=False
)

print("Dashboard dataset created successfully.")
print()
print(f"Rows: {len(dashboard_df)}")
print(f"Columns: {len(dashboard_df.columns)}")
print()
print("Saved to:")
print("dashboard/customer_profitability_dashboard.csv")
print()
print("Churn Risk:")
print(dashboard_df["Churn_Risk"].value_counts())
print()
print("Customer Value Tier:")
print(dashboard_df["Customer_Value_Tier"].value_counts())
print()
print("Optimal Action:")
print(dashboard_df["Optimal_Action"].value_counts())