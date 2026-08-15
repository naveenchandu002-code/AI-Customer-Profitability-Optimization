-- =========================================================
-- Customer Profitability & Decision Optimization SQL
-- =========================================================


-- 1. Overall customer portfolio summary
SELECT
    COUNT(*) AS total_customers,
    ROUND(AVG(Churn_Probability) * 100, 2) AS avg_predicted_churn_pct,
    ROUND(AVG(Customer_Value), 3) AS avg_customer_value,
    ROUND(SUM(Expected_Incremental_Profit), 2) AS total_expected_incremental_profit,
    ROUND(SUM(Intervention_Cost), 2) AS total_intervention_cost
FROM customer_decision;


-- 2. Customer count and churn by recommended action
SELECT
    Recommended_Action,
    COUNT(*) AS customers,
    ROUND(AVG(Churn_Probability) * 100, 2) AS avg_predicted_churn_pct,
    ROUND(AVG(Customer_Value), 3) AS avg_customer_value
FROM customer_decision
GROUP BY Recommended_Action
ORDER BY customers DESC;


-- 3. Customer value tier analysis
SELECT
    CASE
        WHEN Customer_Value < 0.30 THEN 'Low'
        WHEN Customer_Value < 0.60 THEN 'Medium'
        ELSE 'High'
    END AS customer_value_tier,
    COUNT(*) AS customers,
    ROUND(AVG(Churn_Probability) * 100, 2) AS avg_predicted_churn_pct,
    ROUND(AVG(Customer_Value), 3) AS avg_customer_value,
    ROUND(AVG(Total_Trans_Amt), 2) AS avg_transaction_amount
FROM customer_decision
GROUP BY
    CASE
        WHEN Customer_Value < 0.30 THEN 'Low'
        WHEN Customer_Value < 0.60 THEN 'Medium'
        ELSE 'High'
    END
ORDER BY
    avg_customer_value DESC;


-- 4. Optimal-action profitability analysis
SELECT
    Optimal_Action,
    COUNT(*) AS customers,
    ROUND(SUM(Expected_Incremental_Profit), 2) AS expected_incremental_profit,
    ROUND(AVG(Expected_Incremental_Profit), 2) AS avg_expected_profit,
    ROUND(SUM(Intervention_Cost), 2) AS intervention_cost
FROM customer_decision
GROUP BY Optimal_Action
ORDER BY expected_incremental_profit DESC;


-- 5. Top 10 retention opportunities
SELECT
    CLIENTNUM,
    ROUND(Churn_Probability * 100, 2) AS churn_probability_pct,
    ROUND(Customer_Value, 3) AS customer_value,
    ROUND(Expected_Incremental_Profit, 2) AS expected_incremental_profit,
    Intervention_Cost,
    ROUND(Expected_ROI * 100, 2) AS expected_roi_pct
FROM customer_decision
WHERE Optimal_Action = 'RETENTION'
ORDER BY Expected_Incremental_Profit DESC
LIMIT 10;