# Data Pipeline Starter

A complete, beginner-friendly ELT pipeline: **dbt + DuckDB**, built around a
small fake e-commerce dataset. Generate the data, load it, transform it, test
it, and document it, all on your own laptop with zero cloud accounts.

## What this is

Companies keep raw data in messy piles and need clean, trustworthy tables for
dashboards and decisions. This repo is a small working example of that whole
flow, using the same tools real data teams use.

## How it works (the simple version)

Think of it like running a small shop:

1. **Raw zone** (`data/raw/`): delivery boxes pile up at the back door. These
   are the CSV files, exactly as generated. Nobody cleans them, nobody
   renames them.
2. **Staging** (`models/staging/`): you open each box, wipe the dust off, and
   put things on labeled shelves. Light cleaning only: fix date formats, fix
   number formats. One clean view per raw table.
3. **Marts** (`models/marts/`): you build the finished displays the shop owner
   actually looks at. One table per business question, precomputed and fast.

So the flow is: **raw -> staging -> marts**. Each layer only reads from the
one before it. If something looks wrong downstream, you can trace it back
layer by layer.

## Project layout

```
data-pipeline-starter/
  generate_data.py          makes the fake CSVs (stdlib only)
  load_raw.py               loads CSVs into DuckDB as raw_* tables
  requirements.txt          Python packages (dbt-duckdb)
  ecommerce_analytics/
    dbt_project.yml         dbt project settings
    profiles.yml            local DuckDB connection (no secrets)
    ecommerce.duckdb        created when you run the pipeline (gitignored)
    models/
      staging/
        sources.yml         declares the raw tables dbt reads
        stg_customers.sql   cleaned customers
        stg_orders.sql      cleaned orders
        stg_products.sql    cleaned products
        schema.yml          tests for staging
      marts/
        mart_customer_orders.sql  one row per customer, lifetime stats
        mart_daily_revenue.sql    one row per day, revenue stats
        schema.yml                tests for marts
```

## Setup

You need Python 3.9 or newer.

```bash
# 1. Create and activate a virtual environment (keeps things tidy)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# 2. Install the one dependency
pip install -r requirements.txt
```

## Run the pipeline

```bash
# 1. Make the fake data (200 customers, 40 products, 600 orders)
python generate_data.py

# 2. Load the CSVs into DuckDB as raw tables
python load_raw.py

# 3. Build every dbt model (staging views + mart tables)
cd ecommerce_analytics
dbt build --profiles-dir .

# 4. Run the data tests on their own
dbt test --profiles-dir .

# 5. Generate browsable documentation
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .   # opens http://localhost:8080
```

`dbt build` runs models and tests together. `dbt test` runs only the tests.
`dbt docs generate` builds a website describing every model, column, and test.

## What each model answers

| Model | Business question it answers |
|---|---|
| `stg_customers` | (staging) Who are our customers, cleaned up? |
| `stg_products` | (staging) What do we sell, cleaned up? |
| `stg_orders` | (staging) What was ordered, cleaned up? |
| `mart_customer_orders` | Who are our best customers, and how much has each spent? |
| `mart_daily_revenue` | How much money did we make each day? Is revenue trending up? |

## The tests

Tests are promises the data must keep. They live in the `schema.yml` files:

- **not_null / unique**: ids are always filled in and never repeated.
- **relationships**: every order points to a real customer and a real product
  (like a foreign key).
- **accepted_values**: `status` can only be completed, cancelled, refunded, or
  pending; `category` can only be one of the five known categories.

Run `dbt test --profiles-dir .` any time to check every promise.

## Ideas to extend it

- Add a `mart_monthly_revenue` model and compare it with the daily one.
- Add a staging test that `quantity` is greater than zero.
- Point the profile at MotherDuck or a Postgres database instead of a file.
- Schedule `dbt build` with a cron job or GitHub Actions for a daily refresh.

## License

MIT. See [LICENSE](LICENSE).
