import csv
import random
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def read_csv(filename):
    with open(RAW_DIR / filename, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(filename, rows):
    filepath = RAW_DIR / filename

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# Orders
# ============================================================

orders = read_csv("orders.csv")

original_order_count = len(orders)

# 1. Duplicate 100 orders
duplicate_orders = random.sample(orders, 100)

orders.extend(duplicate_orders)

# 2. Invalid customer IDs
for row in random.sample(orders[:original_order_count], 50):
    row["customer_id"] = "9999999"

# 3. Missing customer IDs
for row in random.sample(orders[:original_order_count], 50):
    row["customer_id"] = ""

# 4. Missing store IDs
for row in random.sample(orders[:original_order_count], 25):
    row["store_id"] = ""

write_csv("orders.csv", orders)


# ============================================================
# Order Items
# ============================================================

order_items = read_csv("order_items.csv")

# 5. Negative quantities
for row in random.sample(order_items, 50):
    row["quantity"] = "-1"

# 6. Negative prices
for row in random.sample(order_items, 50):
    row["unit_price"] = "-100"

# 7. Missing product IDs
for row in random.sample(order_items, 50):
    row["product_id"] = "9999999"

write_csv("order_items.csv", order_items)


print("Data quality issues introduced successfully.")

print()
print("Orders:")
print(f"Original rows : {original_order_count:,}")
print(f"Final rows    : {len(orders):,}")
print(f"Duplicates    : {len(orders) - original_order_count:,}")

print()
print("Order Items:")
print(f"Rows          : {len(order_items):,}")
print("Negative qty  : 50")
print("Negative price: 50")
print("Invalid product IDs: 50")