import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

SEED = 42
random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

CUSTOMER_COUNT = 10_000
PRODUCT_COUNT = 1_000
STORE_COUNT = 50
ORDER_COUNT = 100_000

START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 9, 25)

# ============================================================
# Reference Data
# ============================================================

FIRST_NAMES = [
    "Arun", "Karthik", "Rahul", "Vijay", "Suresh",
    "Prakash", "Manoj", "Raj", "Anand", "Deepak",
    "Priya", "Divya", "Anitha", "Meena", "Kavya",
    "Swetha", "Nisha", "Lakshmi", "Pooja", "Revathi"
]

LAST_NAMES = [
    "Kumar", "Sharma", "Rajan", "Krishnan", "Iyer",
    "Reddy", "Nair", "Patel", "Singh", "Menon"
]

CITIES = [
    ("Chennai", "Tamil Nadu"),
    ("Kanchipuram", "Tamil Nadu"),
    ("Coimbatore", "Tamil Nadu"),
    ("Madurai", "Tamil Nadu"),
    ("Trichy", "Tamil Nadu"),
    ("Salem", "Tamil Nadu"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Kochi", "Kerala"),
]

CATEGORIES = {
    "Electronics": ["Mobile", "Laptop", "Tablet", "Headphones"],
    "Home": ["Furniture", "Kitchen", "Storage", "Lighting"],
    "Grocery": ["Rice", "Oil", "Snacks", "Beverages"],
    "Clothing": ["Shirts", "Trousers", "Shoes", "Accessories"],
    "Beauty": ["Skincare", "Haircare", "Makeup", "Personal Care"],
}

BRANDS = [
    "Nova", "Prime", "Max", "Urban", "Fresh",
    "Smart", "Elite", "Classic", "Royal", "Value"
]

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

ORDER_STATUSES = [
    "COMPLETED",
    "SHIPPED",
    "PROCESSING",
    "CANCELLED"
]

# ============================================================
# Helper Functions
# ============================================================


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86399)
    return start_date + timedelta(
        days=random_days,
        seconds=random_seconds
    )


def write_csv(filename, fieldnames, rows):
    filepath = RAW_DIR / filename

    with filepath.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filename}: {len(rows):,} rows")


# ============================================================
# 1. Customers
# ============================================================

def generate_customers():
    rows = []

    for customer_id in range(1, CUSTOMER_COUNT + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        city, state = random.choice(CITIES)

        rows.append({
            "customer_id": customer_id,
            "customer_name": f"{first_name} {last_name}",
            "email": f"customer{customer_id}@example.com",
            "phone": f"9{random.randint(100000000, 999999999)}",
            "city": city,
            "state": state,
            "country": "India",
            "registration_date": random_date(
                datetime(2023, 1, 1),
                END_DATE
            ).date().isoformat()
        })

    write_csv(
        "customers.csv",
        [
            "customer_id",
            "customer_name",
            "email",
            "phone",
            "city",
            "state",
            "country",
            "registration_date"
        ],
        rows
    )


# ============================================================
# 2. Products
# ============================================================

def generate_products():
    rows = []
    product_id = 1

    for category, subcategories in CATEGORIES.items():
        for subcategory in subcategories:
            for _ in range(PRODUCT_COUNT // len(CATEGORIES) // len(subcategories)):
                rows.append({
                    "product_id": product_id,
                    "product_name": f"{random.choice(BRANDS)} {subcategory} {product_id}",
                    "category": category,
                    "subcategory": subcategory,
                    "brand": random.choice(BRANDS),
                    "unit_price": round(
                        random.uniform(50, 100000),
                        2
                    )
                })

                product_id += 1

    write_csv(
        "products.csv",
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "brand",
            "unit_price"
        ],
        rows
    )


# ============================================================
# 3. Stores
# ============================================================

def generate_stores():
    rows = []

    regions = {
        "Tamil Nadu": "South",
        "Karnataka": "South",
        "Telangana": "South",
        "Maharashtra": "West",
        "Delhi": "North",
        "Kerala": "South"
    }

    for store_id in range(1, STORE_COUNT + 1):
        city, state = random.choice(CITIES)

        rows.append({
            "store_id": store_id,
            "store_name": f"Retail Store {store_id}",
            "city": city,
            "state": state,
            "region": regions[state],
            "store_type": random.choice([
                "PHYSICAL",
                "ONLINE"
            ])
        })

    write_csv(
        "stores.csv",
        [
            "store_id",
            "store_name",
            "city",
            "state",
            "region",
            "store_type"
        ],
        rows
    )


# ============================================================
# 4. Orders + Order Items + Payments
# ============================================================

def generate_transactions():

    orders = []
    order_items = []
    payments = []

    order_item_id = 1
    payment_id = 1

    for order_id in range(1, ORDER_COUNT + 1):

        customer_id = random.randint(1, CUSTOMER_COUNT)
        store_id = random.randint(1, STORE_COUNT)

        order_date = random_date(
            START_DATE,
            END_DATE
        )

        status = random.choice(ORDER_STATUSES)
        payment_method = random.choice(PAYMENT_METHODS)

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "store_id": store_id,
            "order_date": order_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "order_status": status,
            "payment_method": payment_method
        })

        item_count = random.randint(1, 5)

        order_total = 0

        for _ in range(item_count):

            product_id = random.randint(
                1,
                PRODUCT_COUNT
            )

            quantity = random.randint(1, 5)

            unit_price = round(
                random.uniform(50, 100000),
                2
            )

            discount = round(
                random.uniform(0, unit_price * 0.20),
                2
            )

            line_amount = round(
                quantity * unit_price - discount,
                2
            )

            order_total += line_amount

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
                "line_amount": line_amount
            })

            order_item_id += 1

        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": order_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "payment_method": payment_method,
            "payment_amount": round(order_total, 2),
            "payment_status": (
                "SUCCESS"
                if status != "CANCELLED"
                else "REFUNDED"
            )
        })

        payment_id += 1

    write_csv(
        "orders.csv",
        [
            "order_id",
            "customer_id",
            "store_id",
            "order_date",
            "order_status",
            "payment_method"
        ],
        orders
    )

    write_csv(
        "order_items.csv",
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "line_amount"
        ],
        order_items
    )

    write_csv(
        "payments.csv",
        [
            "payment_id",
            "order_id",
            "payment_date",
            "payment_method",
            "payment_amount",
            "payment_status"
        ],
        payments
    )


# ============================================================
# 5. Main
# ============================================================

def main():

    print("=" * 60)
    print("Retail Data Generator")
    print("=" * 60)

    generate_customers()
    generate_products()
    generate_stores()
    generate_transactions()

    print("=" * 60)
    print("Dataset generation completed.")
    print(f"Output directory: {RAW_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()