from minio import Minio
from minio.error import S3Error
import json
import io

# MinIO configuration
MINIO_URL = "http://127.0.0.1:9000"  # Update if MinIO is running elsewhere
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

# Step 1: Check if the bucket exists
try:
    if not minio_client.bucket_exists(BUCKET_NAME):
        print(f"Bucket '{BUCKET_NAME}' does not exist. Creating it...")
        minio_client.make_bucket(BUCKET_NAME)
    else:
        print(f"Bucket '{BUCKET_NAME}' already exists.")
except S3Error as e:
    print(f"Error checking or creating bucket: {e}")
    exit(1)

# Step 2: Define JSON events
json_events = [
    {"user_id": 1, "page": "home", "timestamp": "2025-01-09T12:00:00Z"},
    {"user_id": 2, "page": "about", "timestamp": "2025-01-09T12:05:00Z"},
    {"user_id": 3, "page": "contact", "timestamp": "2025-01-09T12:10:00Z"}
]

# Step 3: Write JSON events to MinIO
def write_to_bucket(BUCKET_NAME, minio_client, json_events):
    for i, event in enumerate(json_events):
        try:
        # Convert JSON event to a bytes stream
            event_bytes = io.BytesIO(json.dumps(event).encode("utf-8"))
            object_name = f"event_{i+1}.json"  # Name of the object in MinIO

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

write_to_bucket(BUCKET_NAME, minio_client, json_events)

print("All events uploaded successfully!")
