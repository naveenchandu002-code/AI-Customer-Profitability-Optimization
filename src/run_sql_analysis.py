import sqlite3
import pandas as pd

DB_PATH = "outputs/customer_profitability.db"
SQL_PATH = "src/sql/customer_analysis.sql"

conn = sqlite3.connect(DB_PATH)

with open(SQL_PATH, "r", encoding="utf-8") as f:
    sql_text = f.read()

queries = [
    q.strip()
    for q in sql_text.split(";")
    if q.strip()
]

print("SQL analysis started.")
print(f"Queries found: {len(queries)}")
print()

for i, query in enumerate(queries, start=1):

    # Remove SQL comment lines
    cleaned_lines = [
        line for line in query.splitlines()
        if not line.strip().startswith("--")
    ]

    cleaned_query = "\n".join(cleaned_lines).strip()

    if not cleaned_query:
        continue

    try:
        result = pd.read_sql_query(
            cleaned_query,
            conn
        )

        output_path = f"outputs/sql_query_{i}.csv"
        result.to_csv(
            output_path,
            index=False
        )

        print(f"Query {i} completed.")
        print(result.to_string(index=False))
        print()
        print(f"Saved: {output_path}")
        print("-" * 60)

    except Exception as e:
        print(f"Query {i} failed.")
        print(e)
        print("-" * 60)

conn.close()

print()
print("SQL analysis completed.")