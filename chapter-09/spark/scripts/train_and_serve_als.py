import sys
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import current_timestamp, lit, explode, col

POSTGRES_URL = "jdbc:postgresql://postgres:5432/oneshop"
USERNAME = "postgresuser"
PASSWORD = "postgrespw"

MODEL_VERSION = "v1.0"
TOP_N = 5

try:
    spark = SparkSession.builder \
        .appName("train-and-serve-recommendations") \
        .getOrCreate()
except Exception as e:
    print(f"Error creating SparkSession: {e}")
    sys.exit(1)

print("SparkSession created successfully.")

# --------------------------------------------
# Load ALS training data from Iceberg
# --------------------------------------------
als_input = spark.read.format("iceberg").load("gold.als_training_input") \
    .filter(f"feature_version = '{MODEL_VERSION}'") \
    .select("user_id", "item_id", "interaction_score")

# --------------------------------------------
# Train ALS model
# --------------------------------------------
als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="user_id",
    itemCol="item_id",
    ratingCol="interaction_score",
    implicitPrefs=True,
    coldStartStrategy="drop"
)

model = als.fit(als_input)

# --------------------------------------------
# Generate top-N recommendations per user
# --------------------------------------------
user_recs = model.recommendForAllUsers(TOP_N)

# Flatten recommendations into rows
flattened = user_recs.selectExpr("user_id", "explode(recommendations) as rec") \
    .select(
        col("user_id"),
        col("rec.item_id"),
        col("rec.rating").alias("score")
    )

# Add metadata
enriched_recs = flattened.withColumn("generated_at", current_timestamp()) \
    .withColumn("model_version", lit(MODEL_VERSION))


# --------------------------------------------
# Save to Postgres for real-time serving
# --------------------------------------------
enriched_recs.write \
    .format("jdbc") \
    .option("url", POSTGRES_URL) \
    .option("dbtable", "user_recommendations") \
    .option("user", USERNAME) \
    .option("password", PASSWORD) \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

print("✅ ALS recommendations written to Postgres (user_recommendations)")

# --- Stop Spark Session ---
spark.stop()
print("Spark Session stopped.")