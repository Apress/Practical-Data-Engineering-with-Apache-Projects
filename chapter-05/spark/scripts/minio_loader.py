import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

minio_access_key = "admin"
minio_secret_key = "password"
minio_endpoint = "http://minio:9000"
minio_bucket = "pageviews"

try:
    spark = SparkSession.builder \
        .appName("minio-to-iceberg-loader") \
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint) \
        .config("spark.hadoop.fs.s3a.access.key", minio_access_key) \
        .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
except Exception as e:
    print(f"Error creating SparkSession: {e}")
    sys.exit(1)

print("SparkSession created successfully.")

try:
    print("Reading pageview events from MinIO...")
    pageviews_df = spark.read.json(f"s3a://{minio_bucket}/")

    pageviews_df = pageviews_df.select(
        col("user_id").cast("long"),
        col("url").cast("string"),
        col("channel").cast("string"),
        col("received_at").cast("timestamp")
    )

    # Write to Iceberg table. 'overwrite' mode is used for initial load.
    pageviews_df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .option("format-version", "2") \
        .save("bronze.pageviews")
    
    print("'pageviews' bucket content loaded successfully into Iceberg.")
except Exception as e:
    print(f"Error processing pageview events: {e}")
    sys.exit(1)