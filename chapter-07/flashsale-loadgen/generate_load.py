import math
import os
import random
import time

import barnum
import psycopg2
from psycopg2 import sql, Error

# CONFIG
users_seed_count = 10000
item_seed_count = 1000

item_inventory_min = 1000
item_inventory_max = 5000
item_price_min = 5
item_price_max = 500

purchase_gen_count = 100 
purchase_gen_every_ms = 100

channels = ["organic search", "paid search", "referral", "social", "display"]
categories = ["widgets", "gadgets", "doodads", "clearance"]
campaigns = ["BOGO23", "FLASH2025"]

postgres_host = os.getenv("POSTGRES_HOST", "postgres")
postgres_port = os.getenv("POSTGRES_PORT", "5432")
postgres_user = os.getenv("POSTGRES_USER", "postgresuser")
postgres_pass = os.getenv("POSTGRES_PASSWORD", "postgrespw")
postgres_db = os.getenv("POSTGRES_DB", "oneshop")

# INSERT TEMPLATES
item_insert = "INSERT INTO items (name, category, price, inventory) VALUES (%s, %s, %s, %s)"
user_insert = "INSERT INTO users (first_name, last_name, email, is_vip) VALUES (%s, %s, %s, %s)"
purchase_insert = "INSERT INTO purchases (user_id, item_id, campaign_id, quantity, purchase_price, created_at) VALUES (%s, %s, %s, %s, %s, %s)"

try:
    with psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        user=postgres_user,
        password=postgres_pass,
        dbname=postgres_db
    ) as connection:
        with connection.cursor() as cursor:
            print("Seeding data...")
            cursor.executemany(
                item_insert,
                [
                    (
                        barnum.create_nouns(),
                        random.choice(categories),
                        random.randint(item_price_min * 100, item_price_max * 100) / 100,
                        random.randint(item_inventory_min, item_inventory_max),
                    )
                    for i in range(item_seed_count)
                ],
            )
            cursor.executemany(
                user_insert,
                [
                    (barnum.create_name()[0], barnum.create_name()[1], barnum.create_email(), (random.randint(0, 10) > 8))
                    for i in range(users_seed_count)
                ],
            )
            connection.commit()

            print("Getting item ID and PRICEs...")
            cursor.execute("SELECT id, price FROM items")
            item_prices = [(row[0], row[1]) for row in cursor.fetchall()]

            print("Preparing to seed purchases")
            purchase_rows = []
            for i in range(purchase_gen_count): 
                # Get a user and item to purchase
                purchase_item = random.choice(item_prices)
                purchase_user = random.randint(0, users_seed_count - 1)
                purchase_quantity = random.randint(1, 5)
                campaign_id = random.choice(campaigns)
                purchase_ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(0, 24 * 60 * 60)))

                # Add purchase row to batch
                purchase_rows.append(
                    (
                        purchase_user,
                        purchase_item[0],
                        campaign_id,
                        purchase_quantity,
                        purchase_item[1] * purchase_quantity,
                        purchase_ts
                    )
                )

                # Pause
                time.sleep(purchase_gen_every_ms / 1000)

            # Execute batch insert and commit
            cursor.executemany(purchase_insert, purchase_rows)
            connection.commit()

    connection.close()
except Error as e:
    print(e)
