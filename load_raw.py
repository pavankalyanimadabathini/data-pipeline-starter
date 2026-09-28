"""Load the raw CSV files into DuckDB as tables.

Run this after generate_data.py:
    python load_raw.py

It reads each CSV under data/raw/ and creates (or replaces) a matching table
inside the local DuckDB database file:
    customers.csv  ->  raw_customers
    products.csv   ->  raw_products
    orders.csv     ->  raw_orders

Think of this step as "unloading the delivery truck into the warehouse".
The CSVs are the boxes, DuckDB is the warehouse, and the raw_ tables are
the shelves where boxes sit untouched. dbt will do the organizing later.

Requires the `duckdb` package (installed via requirements.txt).
"""

import os
import duckdb

# The DuckDB file lives inside the dbt project folder so the dbt profile
# (profiles.yml) and this script always point at the same database.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ecommerce_analytics", "ecommerce.duckdb")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

# Each pair is (csv file name, table name inside DuckDB).
TABLES = [
    ("customers.csv", "raw_customers"),
    ("products.csv", "raw_products"),
    ("orders.csv", "raw_orders"),
]


def main():
    con = duckdb.connect(DB_PATH)
    for csv_name, table_name in TABLES:
        csv_path = os.path.join(RAW_DIR, csv_name)
        # read_csv sniffs the file and picks sensible column types
        # (dates become DATE, prices become DECIMAL, and so on).
        con.execute(
            f"CREATE OR REPLACE TABLE {table_name} "
            f"AS SELECT * FROM read_csv('{csv_path}', header=true)"
        )
        count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Loaded {count} rows into {table_name}")
    con.close()
    print(f"Done. Database written to {DB_PATH}")


if __name__ == "__main__":
    main()
