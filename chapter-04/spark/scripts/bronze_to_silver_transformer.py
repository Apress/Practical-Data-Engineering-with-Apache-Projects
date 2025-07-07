from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, upper, regexp_extract, lit, when
from pyspark.sql.functions import hour, to_date

# Initialize Spark session with Iceberg support
spark = (
    SparkSession.builder
    .appName("bronze-to-silver-transformer")
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")
    .getOrCreate()
)

bronze_users = spark.table("bronze.users")
bronze_items = spark.table("bronze.items")
bronze_purchases = spark.table("bronze.purchases")
bronze_pageviews = spark.table("bronze.pageviews")

# Define a simple email validation regex (basic, can be improved)
email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

# Transformations:
silver_users = (
    bronze_users
    .withColumn("valid_email", col("email").rlike(email_regex))
    .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name")))
)

silver_items = (
    bronze_items
    .withColumn("price", 
        when(col("price") < 0, lit(0)).otherwise(col("price"))
    )
    .withColumn("category", upper(col("category")))
)

# Join and enrich the purchases table
silver_purchases = (
    bronze_purchases
    .join(bronze_users, bronze_purchases.user_id == bronze_users.id, "left")
    .join(bronze_items, bronze_purchases.item_id == bronze_items.id, "left")
    .select(
        bronze_purchases.id,
        bronze_purchases.user_id,
        bronze_purchases.item_id,
        bronze_purchases.quantity,
        bronze_purchases.purchase_price,
        (col("quantity") * col("purchase_price")).alias("total_price"),
        bronze_users.email.alias("user_email"),
        bronze_items.name.alias("item_name"),
        bronze_items.category.alias("item_category"),
        to_date(bronze_purchases.created_at).alias("purchase_date"),
        hour(bronze_purchases.created_at).alias("purchase_hour"),
        bronze_purchases.created_at,
        bronze_purchases.updated_at
    )
)

# The url format is "/{page_name}/{item_id}"
# Extract page_name and item_id using regex
pageviews_with_item = bronze_pageviews.withColumn(
    "page", regexp_extract(col("url"), r"^/([^/]+)/\d+$", 1)
).withColumn(
    "item_id", regexp_extract(col("url"), r"/(\d+)$", 1).cast("bigint")
).filter(col("item_id").isNotNull())

# Join with items to get item_name and item_category
silver_pageviews_by_items = (
    pageviews_with_item
    .join(bronze_items, pageviews_with_item.item_id == bronze_items.id, "left")
    .select(
        pageviews_with_item.user_id,
        pageviews_with_item.item_id,
        pageviews_with_item.page,
        bronze_items.name.alias("item_name"),
        bronze_items.category.alias("item_category"),
        pageviews_with_item.channel,
        pageviews_with_item.received_at
    )
)

# Write to silver.users Iceberg table (overwrite or append as needed)
(
    silver_users
    .select(
        "id",
        "first_name",
        "last_name",
        "email",
        "created_at",
        "updated_at",
        "valid_email",
        "full_name"
    )
    .writeTo("silver.users")
    .overwritePartitions()
)

# Write to silver.items Iceberg table (overwrite or append as needed)
(
    silver_items
    .select(
        "id",
        "name",
        "category",
        "price",
        "inventory",
        "created_at",
        "updated_at"
    )
    .writeTo("silver.items")
    .overwritePartitions()
)

# Write to silver.purchases Iceberg table (overwrite or append as needed)
(
    silver_purchases
    .writeTo("silver.purchases_enriched")
    .overwritePartitions()
)

# Write to silver.pageviews_by_items Iceberg table
(
    silver_pageviews_by_items
    .writeTo("silver.pageviews_by_items")
    .overwritePartitions()
)

spark.stop()