import psycopg2
from sentence_transformers import SentenceTransformer

# PostgreSQL connection settings
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": 5432,
}

# Load Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT review_id, review FROM public.reviews")
    reviews = cur.fetchall()

    for review_id, review_text in reviews:
        embedding = model.encode(review_text).tolist()

        # Update the table with generated embedding
        cur.execute(
            "UPDATE public.reviews SET review_embedding = %s WHERE review_id = %s;",
            (embedding, review_id),
        )
        conn.commit()
        print("Embeddings updated successfully.")
    
finally:
    cur.close()
    if conn is not None:
        conn.close()