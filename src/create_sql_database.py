import sqlite3
import pandas as pd

CSV_PATH = "dashboard/customer_profitability_dashboard.csv"
DB_PATH = "outputs/customer_profitability.db"

# Load dashboard dataset
df = pd.read_csv(CSV_PATH)

# Create SQLite database
conn = sqlite3.connect(DB_PATH)

# Create/replace the SQL table
df.to_sql(
    "customer_decision",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("SQLite database created successfully.")
print(f"Database: {DB_PATH}")
print(f"Table: customer_decision")
print(f"Rows loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")