
## A gold iceberg table to store computed features

CREATE TABLE IF NOT EXISTS gold.als_training_input (
  user_id INT,
  item_id INT,
  interaction_score FLOAT,
  interaction_type STRING,
  feature_ts TIMESTAMP,
  feature_version STRING
);

## Postgres table to store generated recommedations

dce postgres psql -U postgresuser -d oneshop

CREATE TABLE user_recommendations (
    user_id INT,
    item_id INT,
    score FLOAT,
    model_version TEXT,
    generated_at TIMESTAMP,
    PRIMARY KEY (user_id, item_id)
);

docker compose exec spark-iceberg /opt/spark/bin/spark-submit \
  /home/iceberg/pyspark/scripts/compute_features.py

docker compose exec spark-iceberg /opt/spark/bin/spark-submit \
--jars /home/iceberg/pyspark/jars/postgresql-42.7.6.jar \
  /home/iceberg/pyspark/scripts/train_and_serve_als.py

http://localhost:5050/recommend/69