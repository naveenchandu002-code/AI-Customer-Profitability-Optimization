# Business Insights

## Executive Summary

The analysis covers 10,127 credit-card customers and combines customer behavior, predicted churn risk, customer value, and economic decisioning.

The key objective is not simply to predict churn, but to determine **which customers are economically worth targeting and what intervention should be prioritized**.

---

## 1. Portfolio Overview

- Total customers: **10,127**
- Average predicted churn probability: **15.78%**
- Average customer value score: **0.315**
- Total modeled expected incremental profit: **7,568.99**
- Total modeled intervention cost for economically positive retention customers: **22,900**

The portfolio contains a meaningful high-risk segment, but risk alone does not determine whether the company should spend money on a customer.

---

## 2. Customer Engagement Is a Major Churn Signal

The machine-learning model indicates that customer engagement variables are among the strongest predictors of churn.

Important variables include:

- Total transaction count
- Total transaction amount
- Revolving balance
- Transaction change
- Relationship count
- Months inactive
- Contact frequency

This suggests that declining customer activity can act as an important early-warning signal.

**Business implication:** monitor engagement deterioration and prioritize intervention before customers become fully inactive.

---

## 3. Low-Value Customers Have Higher Predicted Churn

Customer value segmentation shows:

| Value Tier | Customers | Avg. Predicted Churn |
|---|---:|---:|
| High | 700 | 6.03% |
| Medium | 4,655 | 7.69% |
| Low | 4,772 | 25.10% |

Low-value customers have substantially higher predicted churn.

However, high churn does **not automatically justify retention spending**. The company should compare expected customer value against intervention cost.

**Business implication:** use economic attractiveness, not churn probability alone, to determine retention priority.

---

## 4. Prediction Alone Is Not Enough

The rule-based decision engine initially identified:

- 38 customers for direct retention
- 653 for upsell
- 3,855 for cross-sell
- 4,524 for engagement
- 1,057 for no action

After applying customer economics, only **229 customers** generated positive modeled retention economics.

This demonstrates an important business principle:

> **A customer can have high churn risk without being economically worth saving.**

The decision system therefore moves from:

**Prediction → Economic Decision**

rather than stopping at churn prediction.

---

## 5. Retention Opportunity

The optimization layer identifies **229 customers** with positive modeled retention economics.

Average expected incremental value per economically positive customer is approximately:

**33.05**

The highest-priority customers combine:

- High churn probability
- High customer value
- Positive expected incremental profit

These customers represent the strongest candidates for targeted retention investment.

---

## 6. Budget-Constrained Optimization

Under a **$10,000 retention budget**:

- Customers selected: **100**
- Budget spent: **$10,000**
- Expected incremental value: **$5,387.43**
- Expected ROI: **53.87%**

The optimized targeting strategy outperformed random selection across tested budgets.

| Budget | Optimized Value | Random Average | Lift |
|---:|---:|---:|---:|
| $5,000 | 3,620.90 | 1,641.09 | 1,979.81 |
| $10,000 | 5,387.43 | 3,307.92 | 2,079.52 |
| $15,000 | 6,689.72 | 4,977.58 | 1,712.14 |
| $20,000 | 7,427.71 | 6,626.40 | 801.31 |

This indicates that targeted allocation can generate higher modeled value than random allocation under the current assumptions.

---

## 7. Recommended Strategy

### Priority 1 — High-value, high-risk customers

Target customers with:

- High predicted churn
- High customer value
- Positive expected retention economics

Use personalized retention interventions.

### Priority 2 — Monitor high-value, low-risk customers

Avoid unnecessary retention spending.

Instead, focus on:

- Upsell
- Cross-sell
- Engagement
- Relationship expansion

### Priority 3 — Limit spending on low-value, high-risk customers

Customers with high churn risk but insufficient expected economic value should generally receive:

- Low-cost engagement
- Automated communication
- No expensive retention incentive

---

## 8. Strategic Recommendation

The company should move from a **one-size-fits-all retention strategy** toward a **customer-level decisioning system**.

The proposed framework is:

**Customer Data → Churn Prediction → Customer Value → Economic Evaluation → Budget Optimization → Action**

This allows marketing and retention budgets to be allocated toward customers where the expected economic return is highest.

---

## 9. Important Modeling Assumptions

The dataset does not contain actual bank revenue, servicing cost, retention-offer cost, or campaign-response outcomes.

Therefore:

- Customer value is a modeled proxy.
- Retention success rate is an assumption.
- Intervention cost is an assumption.
- Expected profit is modeled rather than observed accounting profit.

Economic sensitivity analysis shows that results change materially under different assumptions.

Therefore, these outputs should be interpreted as **decision-support scenarios**, not audited financial forecasts.

---

## 10. Final Consulting Takeaway

The strongest insight from the project is:

> **The goal is not to save every customer who may churn. The goal is to identify customers where targeted intervention is expected to create positive incremental economic value under a constrained budget.**

This creates a bridge between:

**Analytics → Economics → Decisioning → Business Action**