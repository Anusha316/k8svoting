import redis
import psycopg2
import time

def connect_postgres():
    while True:
        try:
            conn = psycopg2.connect(host="postgres", database="votes", user="postgres", password="password")
            print("Connected to postgres! ✅")
            return conn
        except Exception as e:
            print(f"Waiting for postgres... {e}")
            time.sleep(2)

def create_table(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS votes (id SERIAL PRIMARY KEY, vote VARCHAR(10))")
    conn.commit()
    cur.close()
    print("Table ready! ✅")

def main():
    print("Worker starting...")
    r = redis.Redis(host='redis', port=6379)
    conn = connect_postgres()
    create_table(conn)
    print("Watching redis for votes...")

    while True:
        try:
            cat_votes = int(r.get('cat') or 0)
            dog_votes = int(r.get('dog') or 0)

            cur = conn.cursor()
            cur.execute("DELETE FROM votes")
            for _ in range(cat_votes):
                cur.execute("INSERT INTO votes (vote) VALUES ('cat')")
            for _ in range(dog_votes):
                cur.execute("INSERT INTO votes (vote) VALUES ('dog')")
            conn.commit()
            cur.close()
            print(f"Synced → Cat: {cat_votes} 🐱  Dog: {dog_votes} 🐶")
        except Exception as e:
            print(f"Error: {e}")
            conn = connect_postgres()

        time.sleep(2)

if __name__ == '__main__':
    main()
