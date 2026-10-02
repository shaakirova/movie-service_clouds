from flask import Flask, jsonify, request, send_from_directory, make_response
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = Flask(__name__)

FRONTEND_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend"
)

# Для запуска нескольких копий backend
INSTANCE_ID = os.getenv("INSTANCE_ID", "backend-default")
PORT = int(os.getenv("PORT", "5000"))


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

    cur.execute(
        "SELECT id, title, genre, rating, status FROM movies ORDER BY id;"
    )

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

    response = make_response(jsonify(movies))
    response.headers["X-Backend-Instance"] = INSTANCE_ID

    return response


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
        (
            data["title"],
            data.get("genre"),
            data.get("rating"),
            data.get("status"),
        ),
    )

    movie_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    response = make_response(
        jsonify(
            {
                "message": "Movie added",
                "id": movie_id,
            }
        ),
        201,
    )

    response.headers["X-Backend-Instance"] = INSTANCE_ID

    return response


if __name__ == "__main__":
    create_table()
    print(f"Starting {INSTANCE_ID} on port {PORT}")
    app.run(debug=False, port=PORT)
