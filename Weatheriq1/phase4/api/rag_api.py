import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import psycopg2
from phase4.embeddings.storage import store_weather_data_and_embedding

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

def query_embedding(text: str):
    return model.encode(text).tolist()


@app.get("/query/")
def search_weather_info(query: str = Query(...)):
    try:
        # Try to fetch & store if not already in DB
        store_weather_data_and_embedding(query)
    except Exception as e:
        print("[INFO] Weather data might already exist, continuing search.")

    try:
        query_emb = query_embedding(query)

        conn = psycopg2.connect(
            dbname="poc",
            user="postgres",
            password="u",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT location, description, embedding <-> %s::vector AS distance
            FROM weather_embeddings
            ORDER BY distance ASC
            LIMIT 3;
        """, (query_emb,))

        results = cur.fetchall()
        cur.close()
        conn.close()

        if not results:
            return {"message": "No similar weather data found."}

        return {
            "matches": [
                {
                    "location": r[0],
                    "description": r[1],
                    "similarity_score": r[2]
                } for r in results
            ]
        }

    except Exception as e:
        print("[ERROR] Vector search failed:", str(e))
        traceback.print_exc()
        return {"error": "Failed to process vector search."}