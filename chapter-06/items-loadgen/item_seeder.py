import random
import psycopg2
import os
import barnum

# Configuration
postgres_host = os.getenv("POSTGRES_HOST", "postgres")
postgres_port = os.getenv("POSTGRES_PORT", "5432")
postgres_user = os.getenv("POSTGRES_USER", "postgresuser")
postgres_pass = os.getenv("POSTGRES_PASSWORD", "postgrespw")
postgres_db = os.getenv("POSTGRES_DB", "oneshop")

CATEGORIES = ["widgets", "gadgets", "doodads", "clearance"]
ITEM_COUNT = 1000
PRICE_MIN = 5
PRICE_MAX = 500
INVENTORY_MIN = 100
INVENTORY_MAX = 5000

def random_item():
    name = barnum.create_nouns()
    category = random.choice(CATEGORIES)
    price = round(random.uniform(PRICE_MIN, PRICE_MAX), 2)
    inventory = random.randint(INVENTORY_MIN, INVENTORY_MAX)
    return (name, category, price, inventory)

def main():
    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_pass
    )
    cur = conn.cursor()
    items = [random_item() for _ in range(ITEM_COUNT)]
    cur.executemany(
        "INSERT INTO items (name, category, price, inventory) VALUES (%s, %s, %s, %s)",
        items
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {ITEM_COUNT} items.")

if __name__ == "__main__":
    main()
    
