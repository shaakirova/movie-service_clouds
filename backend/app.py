from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = Flask(__name__)

FRONTEND_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend"
)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "movies_db"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            rating INTEGER,
            status VARCHAR(50)
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(FRONTEND_FOLDER, "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(FRONTEND_FOLDER, "script.js")


@app.route("/api/movies", methods=["GET"])
def get_movies():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, genre, rating, status FROM movies ORDER BY id;")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    movies = []

    for row in rows:
        movies.append(
            {
                "id": row[0],
                "title": row[1],
                "genre": row[2],
                "rating": row[3],
                "status": row[4],
            }
        )

    return jsonify(movies)


@app.route("/api/movies", methods=["POST"])
def add_movie():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO movies (title, genre, rating, status)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (data["title"], data.get("genre"), data.get("rating"), data.get("status")),
    )

    movie_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Movie added", "id": movie_id}), 201


if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5000)
