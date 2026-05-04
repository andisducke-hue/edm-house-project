import sqlite3
from flask import request, redirect
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/genres")
def genres():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    conn.close()

    return render_template("genres.html", genres=genres)

@app.route("/add_genre", methods=["POST"])
def add_genre():
    name = request.form["name"]
    description = request.form["description"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                   (name, description))

    conn.commit()
    conn.close()

    return redirect("/genres")

@app.route("/delete_genre/<int:id>")
def delete_genre(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM genres WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/genres")

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        youtube_link TEXT,
        artist_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists(id),
        FOREIGN KEY (genre_id) REFERENCES genres(id)
    )
    """)

    conn.commit()
    conn.close()

init_db()

def seed_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                   ("Deep House", "Smooth and chill house"))
    cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                   ("Tech House", "Groovy and rhythmic house"))

    conn.commit()
    conn.close()

seed_data()

if __name__ == "__main__":
    app.run(debug=True)