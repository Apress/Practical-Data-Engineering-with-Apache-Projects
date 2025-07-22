import json
import math
import os
import io
import random
import time
from minio import Minio
from minio.error import S3Error

import barnum
import psycopg2
from psycopg2 import sql, Error
import uuid

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

pageview_multiplier = 75  # Translates to 75x purchases, currently 750/sec or 65M/day

postgres_host = os.getenv("POSTGRES_HOST", "postgres")
postgres_port = os.getenv("POSTGRES_PORT", "5432")
postgres_user = os.getenv("POSTGRES_USER", "postgresuser")
postgres_pass = os.getenv("POSTGRES_PASSWORD", "postgrespw")
postgres_db = os.getenv("POSTGRES_DB", "oneshop")

# MinIO configuration
MINIO_URL = "http://minio:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "password"
BUCKET_NAME = "pageviews"

# Initialize MinIO client
minio_client = Minio(
    MINIO_URL.replace("http://", "").replace("https://", ""),
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)

def delete_bucket():
    try:
        # List and delete all objects in the bucket
        objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
        for obj in objects:
            print(f"Deleting object: {obj.object_name}")
            minio_client.remove_object(BUCKET_NAME, obj.object_name)

        # Delete the bucket
        print(f"Deleting bucket: {BUCKET_NAME}")
        minio_client.remove_bucket(BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} deleted successfully.")
    except S3Error as err:
        print(f"Error: {err}")

# Step 1: Refresh the bucket
try:
    if (minio_client.bucket_exists(BUCKET_NAME)):
        print(f"Bucket '{BUCKET_NAME}' already exists. Deleting it...")
        delete_bucket() 
    
    print(f"Creating bucket '{BUCKET_NAME}'...")
    minio_client.make_bucket(BUCKET_NAME)
    print(f"Bucket '{BUCKET_NAME}' created.")
except S3Error as e:
    print(f"Error checking, deleting, or creating bucket: {e}")
    exit(1)

# INSERT TEMPLATES
item_insert = "INSERT INTO items (name, category, price, inventory) VALUES (%s, %s, %s, %s)"
user_insert = "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
purchase_insert = "INSERT INTO purchases (user_id, item_id, quantity, purchase_price, created_at) VALUES (%s, %s, %s, %s, %s)"

def generatePageview(viewer_id, target_id, page_type):
    return {
        "user_id": viewer_id,
        "url": f"/{page_type}/{target_id}",
        "channel": random.choice(channels),
        "received_at": int(time.time()),
    }

def write_to_bucket(event):
    try:
        # Convert JSON event to a bytes stream
        event_bytes = io.BytesIO(json.dumps(event).encode("utf-8"))
        # Name of the object in MinIO
        object_name = f"event_{int(time.time())}_{uuid.uuid4()}.json"

        # Upload the object to the bucket
        minio_client.put_object(
            BUCKET_NAME,
            object_name,
            data=event_bytes,
            length=event_bytes.getbuffer().nbytes,
            content_type="application/json"
        )
        print(f"Uploaded: {object_name}")

    except S3Error as e:
        print(f"Error uploading {object_name}: {e}")

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
                    (
                        barnum.create_name()[0],
                        barnum.create_name()[1],
                        None if random.random() < 0.1 else barnum.create_email()  # 10% chance of null email
                    )
                    for i in range(users_seed_count)
                ],
            )
            connection.commit()

            print("Getting item ID and PRICEs...")
            cursor.execute("SELECT id, price FROM items")
            item_prices = [(row[0], row[1]) for row in cursor.fetchall()]

            print("Preparing to loop + seed kafka pageviews and purchases")
            for i in range(purchase_gen_count): 
                # Get a user and item to purchase
                purchase_item = random.choice(item_prices)
                purchase_user = random.randint(0, users_seed_count - 1)
                purchase_quantity = random.randint(1, 5)
                purchase_ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(0, 24 * 60 * 60)))
                
                # Write purchaser pageview
                write_to_bucket(generatePageview(purchase_user, purchase_item[0], "products"))

                # Write random pageviews to products or profiles
                pageview_oscillator = int(
                    pageview_multiplier + (math.sin(time.time() / 1000) * 50)
                )
                for i in range(pageview_oscillator):
                    rand_user = random.randint(0, users_seed_count)
                    page_type = "products"
                    
                    # write to bucket
                    write_to_bucket(generatePageview(
                        rand_user,
                        random.randint(0, item_seed_count),
                        page_type,
                    ))
                
                # Write purchase row
                cursor.execute(
                    purchase_insert,
                    (
                        purchase_user,
                        purchase_item[0],
                        purchase_quantity,
                        purchase_item[1] * purchase_quantity,
                        purchase_ts
                    ),
                )
                connection.commit()

                # Pause
                time.sleep(purchase_gen_every_ms / 1000)

    connection.close()
except Error as e:
    print(e)
