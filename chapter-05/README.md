

Seed the segments

dce spark-iceberg python /home/iceberg/scripts/segments_seeder.py

## DuckDB test
SELECT count(*)
FROM iceberg_scan('s3://warehouse/segmentation/customers/metadata/00000-8695e124-6461-4af5-b485-a2f817a006e1.metadata.json');

SET s3_endpoint = 'minio:9000';

SET s3_access_key_id = 'admin';
SET s3_secret_access_key = 'password';
SET s3_url_style = 'path';
SET s3_use_ssl = false;

## PyIceberg from tester container

export AWS_ACCESS_KEY_ID=admin
export AWS_SECRET_ACCESS_KEY=password


{
  "protocol": "https",
  "verify": "false"
}

from trino.dbapi import connect

conn = connect(
    host="trino",
    port=8080,
    user="admin",
    catalog="iceberg",
    schema="gold",
)
cur = conn.cursor()
cur.execute("SELECT * FROM system.runtime.nodes")
rows = cur.fetchall()

## Enabling HTTPS

keytool -genkeypair \
  -alias trino \
  -keyalg RSA \
  -keystore keystore.jks \
  -storepass trino123 \
  -keypass trino123 \
  -dname "CN=localhost, OU=Test, O=Test, L=City, S=State, C=US"

vO6LSUYT1eUTRp24pilLAd0UacoktqBNNzLSf3BhJt96MUSo37BewD9pcBxGqPRNoKOhElpiUEo6w8XODzp1WbLXwgcryeUXVaSLEV9PMfs1Ie8kPJNj3pOgJAKOO+3aPxxYEpymjsiA4zFlIhEw4lR1BmPZQz3KXsmEM3ee79Ls5PPTnaNWKN2ePMCMOfaDpRg3MCe8ghKjHlfQK2/t6tNAwwQw2XrNead8hov4YECrXpuX4BK9ib2YPv0WLqPxB96dBK/LkOMWhu3vNka+zrtJlpX63tqVYinSZW5OD2DjnPhJGR82gCyYDwA00QKqTeTfJn1R1u8W7bDdg1QjJyOX+lKKGcz7fftVo40RiVPvb2SecOflxjNCsoS1D9WsQQvRtdZ+kcEIyQ7+A9ysNNrFRhAfxJEzevx6HOLTJrSjObGYh+eegbmC40crFjUWPXKtQbSbWtTfYa2mjtylmqziiY6Ww9nt58cMDey1N5HeqhLxmAX+venI08cPQCuneDrwpAF9fqJW75yB3Pi0VIVXwYNXgXyFij1i2iiXfT71WHg8gN6GWmAnbXQ8TA+d4zk12bOW2sVH0Yz6CNgVFdd/K1Hv5wqwduvNz+ZovDRLyLqnIpKL4P1kRdwFsX/Ad5wwkxJ49lpqDvDnrOsms6wN3ebHgZxQVUwmCUkx0k4=


bcrypt passwords start with $2y$ and must use a minimum cost of 8:
test:$2y$10$BqTb8hScP5DfcpmHo5PeyugxHz5Ky/qf3wrpD7SNm8sWuA3VlGqsa

user:test
password: password
https://github.com/trinodb/trino/issues/11314

Mailhog
localhost:8025
Don't use STARTTLS