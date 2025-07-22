from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, coalesce, lit, current_timestamp
from pyspark.ml.feature import StringIndexer
import logging

FEATURE_VERSION = "v1.0"

# Initialize Spark session with Iceberg support
spark = (
    SparkSession.builder
    .appName("als-feature-extractor")
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")
    .getOrCreate()
)

purchases = spark.table("silver.purchases_enriched")
pageviews = spark.table("silver.pageviews_by_items")

# --------------------------------------------
# Aggregate Views
# --------------------------------------------
view_counts = pageviews.groupBy("user_id", "item_id") \
    .agg(count("*").alias("view_count"))

# --------------------------------------------
# Aggregate Purchases
# --------------------------------------------
purchase_counts = purchases.groupBy("user_id", "item_id") \
    .agg(count("*").alias("purchase_count"))

# --------------------------------------------
# Join Views and Purchases
# --------------------------------------------
interactions = view_counts.join(purchase_counts,
                                on=["user_id", "item_id"],
                                how="outer") \
    .withColumn("view_count", coalesce(col("view_count"), lit(0))) \
    .withColumn("purchase_count", coalesce(col("purchase_count"), lit(0)))
    
# --------------------------------------------
# Compute Interaction Score
# --------------------------------------------
# You can tune weights: views=1, purchases=3
interactions = interactions.withColumn(
    "interaction_score",
    col("view_count") * lit(1.0) + col("purchase_count") * lit(3.0)
)

# --------------------------------------------
# Convert IDs to Integer (ALS requires integer IDs)
# --------------------------------------------

user_indexer = StringIndexer(inputCol="user_id", outputCol="user_idx", handleInvalid="skip")
item_indexer = StringIndexer(inputCol="item_id", outputCol="item_idx", handleInvalid="skip")

indexed_model = user_indexer.fit(interactions)
interactions = indexed_model.transform(interactions)

indexed_model = item_indexer.fit(interactions)
interactions = indexed_model.transform(interactions)

# --------------------------------------------
# Enrich with metadata for Gold layer
# --------------------------------------------

final_df = interactions.select(
    col("user_idx").cast("int").alias("user_id"),
    col("item_idx").cast("int").alias("item_id"),
    col("interaction_score").cast("float"),
    lit("composite").alias("interaction_type"),
    current_timestamp().alias("feature_ts"),
    lit(FEATURE_VERSION).alias("feature_version")
)
final_df.write.format("iceberg").mode("overwrite").save("gold.als_training_input")

record_count = final_df.count()

logging.basicConfig(level=logging.INFO)
logging.info(f"ALS training dataset with {final_df.count()} records written to Iceberg table: gold.als_training_input")