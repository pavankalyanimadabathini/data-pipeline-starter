"""Generate a small, realistic e-commerce dataset as CSV files.

Run this once:
    python generate_data.py

It creates three files under data/raw/:
    customers.csv   one row per customer
    products.csv    one row per product
    orders.csv      one row per order

The data is fake but realistic, and it is deterministic: the random seed is
fixed, so you get the exact same rows every time you run it. That makes the
pipeline easy to test and debug.

Only the Python standard library is used here (csv, random, datetime),
so this script runs anywhere Python runs.
"""

import csv
import os
import random
from datetime import date, timedelta

# Fixed seed = same data on every run. Change it if you want different data.
RANDOM_SEED = 42

NUM_CUSTOMERS = 200
NUM_PRODUCTS = 40
NUM_ORDERS = 600

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")

FIRST_NAMES = [
    "Aarav", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Krishna", "Meera",
    "Nikhil", "Priya", "Rahul", "Riya", "Rohan", "Sanya", "Vikram", "Zara",
    "Aditya", "Divya", "Farhan", "Gauri", "Harsh", "Ira", "Jay", "Kiran",
    "Lakshmi", "Manoj", "Neha", "Om", "Pooja", "Raj",
]

LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Gupta", "Mehta", "Khan", "Iyer", "Nair",
    "Singh", "Das", "Kulkarni", "Joshi", "Chopra", "Verma", "Rao", "Menon",
    "Pillai", "Agarwal", "Bose", "Chandra",
]

COUNTRIES = ["USA", "India", "UK", "Canada", "Australia", "Germany"]

PRODUCT_ADJECTIVES = [
    "Classic", "Pro", "Ultra", "Eco", "Deluxe", "Compact", "Smart", "Prime",
    "Essential", "Supreme",
]

CATEGORIES = ["Electronics", "Apparel", "Home", "Books", "Sports"]

# Nouns grouped by category so product names make sense
# ("Trail Backpack" is Apparel, not Electronics).
CATEGORY_NOUNS = {
    "Electronics": ["Headphones", "Keyboard", "Speaker", "Drone", "Monitor",
                    "Smart Watch", "Earbuds", "Tablet"],
    "Apparel": ["Backpack", "Jacket", "Shoes", "Sunglasses", "Wallet",
                "Hat", "Scarf", "Belt"],
    "Home": ["Lamp", "Mug", "Chair", "Bottle", "Blender", "Cushion",
             "Vase", "Rug"],
    "Books": ["Novel", "Notebook", "Cookbook", "Atlas", "Journal",
              "Comic", "Textbook", "Poetry Collection"],
    "Sports": ["Tent", "Yoga Mat", "Dumbbell", "Racket", "Football",
               "Gloves", "Skipping Rope", "Gym Bag"],
}

# Order statuses and how often each one shows up (weights add up to 100).
ORDER_STATUSES = ["completed", "completed", "completed", "completed",
                  "completed", "completed", "completed", "completed",
                  "cancelled", "refunded", "pending"]


def random_date(start, end):
    """Pick a random date between start and end (inclusive)."""
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def make_customers():
    rows = []
    for i in range(1, NUM_CUSTOMERS + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        rows.append({
            "customer_id": f"C{i:04d}",
            "first_name": first,
            "last_name": last,
            # The number at the end guarantees every email is unique.
            "email": f"{first}.{last}{i}@example.com".lower(),
            "country": random.choice(COUNTRIES),
            "signup_date": random_date(date(2024, 1, 1), date(2024, 12, 31)).isoformat(),
        })
    return rows


def make_products():
    rows = []
    used_names = set()
    i = 1
    while len(rows) < NUM_PRODUCTS:
        category = random.choice(CATEGORIES)
        name = f"{random.choice(PRODUCT_ADJECTIVES)} {random.choice(CATEGORY_NOUNS[category])}"
        # Product names must be unique, so skip names we already used.
        if name in used_names:
            continue
        used_names.add(name)
        rows.append({
            "product_id": f"P{i:03d}",
            "product_name": name,
            "category": category,
            "unit_price": f"{random.uniform(5.0, 500.0):.2f}",
        })
        i += 1
    return rows


def make_orders(customer_ids, product_ids):
    rows = []
    for i in range(1, NUM_ORDERS + 1):
        rows.append({
            "order_id": f"O{i:05d}",
            "customer_id": random.choice(customer_ids),
            "product_id": random.choice(product_ids),
            "quantity": random.randint(1, 5),
            "order_date": random_date(date(2025, 1, 1), date(2025, 6, 30)).isoformat(),
            "status": random.choice(ORDER_STATUSES),
        })
    return rows


def main():
    random.seed(RANDOM_SEED)
    os.makedirs(RAW_DIR, exist_ok=True)

    customers = make_customers()
    products = make_products()
    orders = make_orders(
        [c["customer_id"] for c in customers],
        [p["product_id"] for p in products],
    )

    write_csv(os.path.join(RAW_DIR, "customers.csv"),
              ["customer_id", "first_name", "last_name", "email", "country", "signup_date"],
              customers)
    write_csv(os.path.join(RAW_DIR, "products.csv"),
              ["product_id", "product_name", "category", "unit_price"],
              products)
    write_csv(os.path.join(RAW_DIR, "orders.csv"),
              ["order_id", "customer_id", "product_id", "quantity", "order_date", "status"],
              orders)

    print("Done. Raw data is ready under data/raw/.")


if __name__ == "__main__":
    main()
