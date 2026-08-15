# AI-Driven Customer Profitability & Decision Optimization

## Executive Summary

A data-driven customer decisioning project for a global credit-card company.

The objective is to answer:

> **Which customers should the company target, what action should it take, and how can it maximize incremental value under a fixed budget?**

The project combines:

**Customer Analytics → Machine Learning → Customer Value → Economic Decisioning → Optimization → Power BI**

---

## Business Problem

A credit-card company has a large customer base but limited resources for retention, engagement, upselling, and cross-selling.

The company needs to avoid treating every customer equally.

The decision system identifies:

- Who is likely to churn
- Which customers have higher modeled value
- Which intervention is economically justified
- Which customers should receive no intervention
- How to allocate a fixed retention budget

---

## Project Objective

Build a customer-level decision optimization framework that:

1. Predicts churn risk
2. Estimates customer value
3. Evaluates intervention economics
4. Selects the optimal action
5. Optimizes customer targeting under a budget constraint
6. Communicates decisions through an executive dashboard

---

## Analytical Framework

```text
Customer Data
      ↓
Data Cleaning & EDA
      ↓
Customer Segmentation
      ↓
Customer Value Modeling
      ↓
XGBoost Churn Prediction
      ↓
OOF Churn Probabilities
      ↓
SHAP Explainability
      ↓
Action Decision Engine
      ↓
Economic Evaluation
      ↓
Budget Optimization
      ↓
Sensitivity Analysis
      ↓
Power BI Executive Dashboard