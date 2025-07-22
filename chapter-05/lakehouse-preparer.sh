#!/bin/bash

set -e

echo "Running notebook to create Iceberg tables..."
docker compose exec spark-iceberg jupyter execute /home/iceberg/notebooks/create_iceberg_tables.ipynb

echo "Loading data from Postgres to Iceberg..."
docker compose exec spark-iceberg /opt/spark/bin/spark-submit \
  --jars /home/iceberg/pyspark/jars/postgresql-42.7.6.jar \
  /home/iceberg/pyspark/scripts/postgres_loader.py

echo "Loading data from MinIO to Iceberg..."
docker compose exec spark-iceberg /opt/spark/bin/spark-submit \
  --jars /home/iceberg/pyspark/jars/hadoop-aws-3.3.4.jar,/home/iceberg/pyspark/jars/aws-java-sdk-bundle-1.11.1026.jar \
  /home/iceberg/pyspark/scripts/minio_loader.py

echo "Transforming bronze to silver tables..."
docker compose exec spark-iceberg /opt/spark/bin/spark-submit \
  /home/iceberg/pyspark/scripts/bronze_to_silver_transformer.py

echo "Creating gold layer tables in Trino..."
docker compose exec trino trino --server localhost:8080 --file /opt/trino/iceberg-schema-gold.sql

echo "Lakehouse preparation pipeline completed."