from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Postgres connection details
POSTGRES_HOST = "postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "oneshop"
POSTGRES_USER = "postgresuser"
POSTGRES_PASSWORD = "postgrespw"

def get_recommendations(user_id, top_n=10):
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_id, score
        FROM user_recommendations
        WHERE user_id = %s
        ORDER BY score DESC
        LIMIT %s
        """,
        (user_id, top_n)
    )
    results = [{"item_id": row[0], "score": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@app.route("/recommend/<int:user_id>")
def recommend(user_id):
    recommendations = get_recommendations(user_id)
    return jsonify({"user_id": user_id, "recommendations": recommendations})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
