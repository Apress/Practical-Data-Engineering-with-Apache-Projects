import streamlit as st
import psycopg2
from sentence_transformers import SentenceTransformer
import pandas as pd

# PostgreSQL connection settings
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": 5432,
}

@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def find_similar_reviews(query_text, top_n=5):
    model = load_model()
    query_embedding = model.encode(query_text).tolist()

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT customer_name, review, (review_embedding <=> %s::vector) AS similarity
        FROM public.reviews
        ORDER BY similarity ASC
        LIMIT %s;
        """,
        (query_embedding, top_n),
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

st.set_page_config(page_title="Customer Review Search", layout="wide")
st.title("🔍 Search Customer Reviews by Similarity")

query = st.text_area("Enter your review or search text:", "")
top_n = st.slider("Number of similar reviews to show", min_value=1, max_value=10, value=5)

if st.button("Search") and query.strip():
    with st.spinner("Searching for similar reviews..."):
        results = find_similar_reviews(query, top_n)
        if results:
            df = pd.DataFrame(results, columns=["Customer Name", "Review", "Similarity"])
            df["Similarity"] = df["Similarity"].apply(lambda x: f"{x:.4f}")
            st.dataframe(df)
        else:
            st.info("No similar reviews found.")