# phase4/embeddings/storage.py

import psycopg2
from .embedder import get_weather_and_embedding

def store_weather_data_and_embedding(city: str):
    """Store both structured data and vector embedding for a city."""
    weather, description_text, embedding = get_weather_and_embedding(city)

    conn = psycopg2.connect(
        dbname="poc",
        user="postgres",
        password="u",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    try:
        # Insert structured weather
        cur.execute("""
            INSERT INTO weather_structured (
                city, type, timestamp, temperature, humidity,
                pressure, wind_speed, description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            weather["city"], weather["type"], weather["timestamp"],
            weather["temperature"], weather["humidity"],
            weather["pressure"], weather["wind_speed"], weather["description"]
        ))

        # Insert vector
        cur.execute("""
            INSERT INTO weather_embeddings (location, description, embedding)
            VALUES (%s, %s, %s::vector)
        """, (weather["city"], description_text, embedding))

        conn.commit()
        print(f"[✓] Stored weather and embedding for: {city}")
    except Exception as e:
        conn.rollback()
        print(f"[!] Failed to store data for {city}: {e}")
    finally:
        cur.close()
        conn.close()
