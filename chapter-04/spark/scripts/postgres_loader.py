import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

POSTGRES_URL = "jdbc:postgresql://postgres:5432/oneshop"
USERNAME = "etluser"
PASSWORD = "etlpassword"

try:
    spark = SparkSession.builder \
        .appName("postgres-to-iceberg-loader") \
        .getOrCreate()
except Exception as e:
    print(f"Error creating SparkSession: {e}")
    sys.exit(1)

print("SparkSession created successfully.")
        
# --- ETL Process for Each Table ---

# 1. Load users table
print("Processing 'users' table...")
try:
    users_df = spark.read \
        .format("jdbc") \
        .option("driver", "org.postgresql.Driver") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "users") \
        .option("user", USERNAME) \
        .option("password", PASSWORD) \
        .load()

    # Ensure column types match Iceberg schema (optional, but good practice)
    # Cast necessary columns if there are discrepancies, e.g., if Postgres SERIAL was read as INT
    users_df = users_df.select(
        col("id").cast("long"),
        col("first_name").cast("string"),
        col("last_name").cast("string"),
        col("email").cast("string"),
        col("created_at").cast("timestamp"),
        col("updated_at").cast("timestamp")
    )

    # Write to Iceberg table. 'overwrite' mode is used for initial load.
    users_df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .option("format-version", "2") \
        .save("bronze.users")
    print("'users' table loaded successfully into Iceberg.")
except Exception as e:
    print(f"Error loading 'users' table: {e}")

# 2. Load items table
print("Processing 'items' table...")
try:
    items_df = spark.read \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "public.items") \
        .option("user", USERNAME) \
        .option("password", PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    # Cast necessary columns
    items_df = items_df.select(
        col("id").cast("long"),
        col("name").cast("string"),
        col("category").cast("string"),
        col("price").cast("decimal(7,2)"),
        col("inventory").cast("int"),
        col("created_at").cast("timestamp"),
        col("updated_at").cast("timestamp")
    )

    items_df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .option("format-version", "2") \
        .save("bronze.items")
    print("'items' table loaded successfully into Iceberg.")
except Exception as e:
    print(f"Error loading 'items' table: {e}")

# 3. Load purchases table
print("Processing 'purchases' table...")
try:
    purchases_df = spark.read \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "public.purchases") \
        .option("user", USERNAME) \
        .option("password", PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    # Cast necessary columns
    purchases_df = purchases_df.select(
        col("id").cast("long"),
        col("user_id").cast("long"),
        col("item_id").cast("long"),
        col("quantity").cast("int"),
        col("purchase_price").cast("decimal(12,2)"),
        col("created_at").cast("timestamp"),
        col("updated_at").cast("timestamp")
    )

    purchases_df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .option("format-version", "2") \
        .save("bronze.purchases")
    print("'purchases' table loaded successfully into Iceberg.")
except Exception as e:
    print(f"Error loading 'purchases' table: {e}")

# --- Stop Spark Session ---
spark.stop()
print("Spark Session stopped.")