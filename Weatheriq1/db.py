import psycopg2
from psycopg2 import OperationalError

def get_connection():
    try:
        return psycopg2.connect(
            dbname="poc",
            user="postgres",
            password="u",
            host="localhost",
            port="5432"
        )
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        raise