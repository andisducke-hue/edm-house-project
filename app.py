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

@app.route("/edit_genre/<int:id>", methods=["GET", "POST"])
def edit_genre(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        cursor.execute("UPDATE genres SET name=?, description=? WHERE id=?",
                       (name, description, id))
        conn.commit()
        conn.close()
        return redirect("/genres")

    cursor.execute("SELECT * FROM genres WHERE id=?", (id,))
    genre = cursor.fetchone()
    conn.close()

    return render_template("edit_genre.html", genre=genre)

@app.route("/artists")
def artists():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artists")
    artists = cursor.fetchall()

    conn.close()
    return render_template("artists.html", artists=artists)


@app.route("/add_artist", methods=["POST"])
def add_artist():
    name = request.form["name"]
    image = request.form["image"]
    description = request.form["description"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO artists (name, image) VALUES (?, ?)",
        (name, image, description)
    )

    conn.commit()
    conn.close()

    return redirect("/artists")


@app.route("/delete_artist/<int:id>")
def delete_artist(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM artists WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/artists")

@app.route("/edit_artist/<int:id>", methods=["GET", "POST"])
def edit_artist(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]

        cursor.execute("UPDATE artists SET name=? WHERE id=?", (name, id))
        conn.commit()
        conn.close()
        return redirect("/artists")

    cursor.execute("SELECT * FROM artists WHERE id=?", (id,))
    artist = cursor.fetchone()
    conn.close()

    return render_template("edit_artist.html", artist=artist)

@app.route("/tracks")
def tracks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT tracks.id, tracks.title, tracks.youtube_link,
           artists.name, genres.name
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.id
    JOIN genres ON tracks.genre_id = genres.id
    """)

    tracks = cursor.fetchall()

    cursor.execute("SELECT * FROM artists")
    artists = cursor.fetchall()

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    conn.close()

    return render_template("tracks.html", tracks=tracks, artists=artists, genres=genres)

@app.route("/add_track", methods=["POST"])
def add_track():
    title = request.form["title"]
    youtube_link = request.form["youtube_link"]
    artist_id = request.form["artist_id"]
    genre_id = request.form["genre_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
    VALUES (?, ?, ?, ?)
    """, (title, youtube_link, artist_id, genre_id))

    conn.commit()
    conn.close()

    return redirect("/tracks")

@app.route("/delete_track/<int:id>")
def delete_track(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tracks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/tracks")

@app.route("/edit_track/<int:id>", methods=["GET", "POST"])
def edit_track(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        youtube_link = request.form["youtube_link"]
        artist_id = request.form["artist_id"]
        genre_id = request.form["genre_id"]

        cursor.execute("""
        UPDATE tracks
        SET title=?, youtube_link=?, artist_id=?, genre_id=?
        WHERE id=?
        """, (title, youtube_link, artist_id, genre_id, id))

        conn.commit()
        conn.close()
        return redirect("/tracks")

    cursor.execute("SELECT * FROM tracks WHERE id=?", (id,))
    track = cursor.fetchone()

    cursor.execute("SELECT * FROM artists")
    artists = cursor.fetchall()

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    conn.close()

    return render_template("edit_track.html",
                           track=track,
                           artists=artists,
                           genres=genres)
    
@app.route("/playlists")
def playlists():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # pareizi: dabū VISUS playlists
    cursor.execute("""
    SELECT playlists.id, playlists.name, genres.name
    FROM playlists
    JOIN genres ON playlists.genre_id = genres.id
    """)
    playlists = cursor.fetchall()

    # genres dropdownam
    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    conn.close()

    return render_template(
        "playlists.html",
        playlists=playlists,
        genres=genres
    )

@app.route("/add_playlist", methods=["POST"])
def add_playlist():
    name = request.form["name"]
    genre_id = request.form["genre_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO playlists (name, genre_id) VALUES (?, ?)",
        (name, genre_id)
    )

    conn.commit()
    conn.close()

    return redirect("/playlists")

@app.route("/delete_playlist/<int:id>")
def delete_playlist(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM playlists WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/playlists")

@app.route("/playlist/<int:id>")
def playlist_detail(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # dabū playlist
    cursor.execute("SELECT * FROM playlists WHERE id=?", (id,))
    playlist = cursor.fetchone()

    # dabū VISUS trackus ar to pašu genre
    cursor.execute("""
    SELECT tracks.title, artists.name, tracks.youtube_link
    FROM tracks
    JOIN artists ON tracks.artist_id = artists.id
    WHERE tracks.genre_id = ?
    """, (playlist[2],))

    tracks = cursor.fetchall()

    conn.close()

    return render_template("playlist_detail.html",
                           playlist=playlist,
                           tracks=tracks)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # GENRES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)

    # ARTISTS (ar image)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image TEXT,
        about TEXT
    )
    """)

    # TRACKS
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

    # PLAYLISTS (4. tabula)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        genre_id INTEGER,
        FOREIGN KEY (genre_id) REFERENCES genres(id)
    )
    """)

    conn.commit()
    conn.close()

init_db()

def seed_data():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # GENRES
        cursor.execute("SELECT COUNT(*) FROM genres")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Chocago House", "The original house style from Chicago, built on drum machines, simple basslines, and dancefloor-focused grooves"))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Acid House", "A hypnotic house style with squelchy TB-303 basslines, repetitive patterns, and a psychedelic club feel."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Deep House", "Smooth, soulful, and warm house music with deep bass, jazzy chords, and a relaxed groove."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Progressive House", "Builds tension slowly with long breakdowns, evolving melodies, and a big release at the drop."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("French House", "Funky, filtered, disco-based house with chopped samples, strong groove, and polished club energy."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Funky House", "Bright, upbeat house using disco and funk elements, catchy hooks, and a lively dance feel."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Tribal House", "Percussion-heavy house with world-music rhythms, chants, and a strong organic drum presence."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Afro House", "A house style influenced by African percussion, rhythms, and vocal traditions, often deep and rhythmic."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Tropical House", "Light, relaxed house with airy melodies, steel drums, marimbas, and a summer-like mood. "))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Electro House", "Harder, more aggressive house with heavy synths, strong drops, and a sharper electronic edge."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Bass House", "Bass-driven house with punchy low-end, energetic drops, and a more aggressive modern club sound."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Slap House", "A modern, radio-friendly house style with bouncy bass, strong beat, and melodic vocals. "))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Future House", "A modern house style with bright synths, deep bass, and catchy, energetic drop sections. "))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Garage House", "House music with strong vocal influence, swing, and a link to New York and New Jersey club culture. "))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Lo-Fi House", "Raw and dusty house with tape noise, imperfect textures, and a nostalgic underground atmosphere. "))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Deep House", "Smooth, soulful, and warm house music with deep bass, jazzy chords, and a relaxed groove."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Minimal House", "A stripped-down house style that focuses on small details, subtle repetition, and sparse arrangement."))
            cursor.execute("INSERT INTO genres (name, description) VALUES (?, ?)",
                        ("Latin House", "House music mixed with Latin rhythms, percussion, and melodic elements for a vibrant dance sound."))

        cursor.execute("SELECT COUNT(*) FROM artists")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Fred again..",
            "/static/artist_images/fred-again.jpg",
            "UK electronic producer blending house, garage, emotional vocals, and live performance energy."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("FISHER",
            "/static/artist_images/fisher.jpg",
            "Australian tech house DJ known for high-energy club tracks and festival anthems."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("John Summit",
            "/static/artist_images/john-summit.jpg",
            "American house producer combining festival energy with underground tech house influence."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Dom Dolla",
            "/static/artist_images/dom-dolla.jpg",
            "Australian house producer recognized for groovy basslines and modern club records."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Chris Lake",
            "/static/artist_images/chris-lake.jpg",
            "British electronic producer famous for groove-focused house and tech house music."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Mau P",
            "/static/artist_images/mau-p.jpg",
            "Dutch DJ creating energetic club-focused tech house tracks with catchy hooks."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("KREAM",
            "/static/artist_images/kream.jpg",
            "Norwegian producer duo creating melodic deep house and modern dance music."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("MEDUZA",
            "/static/artist_images/meduza.jpg",
            "Italian electronic trio known for emotional deep house and radio crossover hits."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Claptone",
            "/static/artist_images/claptone.jpg",
            "Mysterious house DJ blending deep house grooves with atmospheric melodies."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("MK",
            "/static/artist_images/mk.jpg",
            "Legendary American house producer influential in deep house and vocal house music."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Peggy Gou",
            "/static/artist_images/peggy-gou.jpg",
            "South Korean DJ and producer mixing house, techno, and stylish underground club sounds."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("CamelPhat",
            "/static/artist_images/camelphat.jpg",
            "British electronic duo known for melodic deep house and progressive club tracks."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Vintage Culture",
            "/static/artist_images/vintage-culture.jpg",
            "Brazilian DJ blending deep house, melodic house, and festival-ready electronic music."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Disclosure",
            "/static/artist_images/disclosure.jpg",
            "British electronic duo combining garage, house, and soulful dance production."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("David Guetta",
            "/static/artist_images/david-guetta.jpg",
            "One of the most influential EDM producers, mixing house music with mainstream pop energy."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Robin Schulz",
            "/static/artist_images/robin-schulz.jpg",
            "German DJ famous for melodic deep house remixes and chill dance tracks."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Purple Disco Machine",
            "/static/artist_images/purple-disco-machine.jpg",
            "German producer combining disco, funky house, and retro dance grooves."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Gorgon City",
            "/static/artist_images/gorgon-city.jpg",
            "UK electronic duo blending deep house, garage, and underground club influences."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Ben Hemsley",
            "/static/artist_images/ben-hemsley.jpg",
            "British DJ known for energetic trance-influenced house and rave-inspired sounds."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Jamie Jones",
            "/static/artist_images/jamie-jones.jpg",
            "Influential house and tech house producer associated with underground club culture."))
            
            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)", ("Alan Walker","/static/artist_images/alan-walker.jpg","Norwegian DJ and producer known for melodic electronic music and cinematic house-inspired tracks."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Kygo",
            "/static/artist_images/kygo.jpg",
            "Producer who popularized tropical house with soft piano melodies and relaxed summer vibes."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Avicii",
            "/static/artist_images/avicii.jpg",
            "Legendary Swedish producer who blended progressive house with emotional songwriting and folk influences."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Alesso",
            "/static/artist_images/alesso.jpg",
            "Swedish progressive house producer famous for euphoric festival anthems and melodic drops."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Calvin Harris",
            "/static/artist_images/calvin-harris.jpg",
            "Scottish DJ and producer combining radio-friendly dance music with house and funk influences."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("TheFatRat",
            "/static/artist_images/thefatrat.jpg",
            "Electronic music producer known for melodic EDM, gaming music, and uplifting house-inspired tracks."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Tobu",
            "/static/artist_images/tobu.jpg",
            "Independent electronic producer known for melodic progressive house and uplifting EDM instrumentals from Latvia."))

            cursor.execute("INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            ("Vicetone",
            "/static/artist_images/vicetone.jpg",
            "Dutch electronic duo creating energetic progressive house and melodic festival music."))
            

        # TRACKS
        cursor.execute("SELECT COUNT(*) FROM tracks")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("adore u", "https://www.youtube.com/watch?v=3aFF09jjZwk", 1, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Delilah (pull me out of this)", "https://www.youtube.com/watch?v=8dQw6jG5l8I", 1, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Jungle", "https://www.youtube.com/watch?v=zBp7KBmgsdU", 1, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Losing It", "https://www.youtube.com/watch?v=o3WdLtpWM_c", 2, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("You Little Beauty", "https://www.youtube.com/watch?v=4bP6mL5p2i4", 2, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Atmosphere", "https://www.youtube.com/watch?v=sA6OknupuHM", 2, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Where You Are", "https://www.youtube.com/watch?v=to8s9G2pYw8", 3, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Go Back", "https://www.youtube.com/watch?v=4QO4wX975mY", 3, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Human", "https://www.youtube.com/watch?v=2u8x7A9Qhsk", 3, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Saving Up", "https://www.youtube.com/watch?v=7YvAYIJSSZY", 4, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Rhyme Dust", "https://www.youtube.com/watch?v=7m_xQfF6wQQ", 4, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("girl$", "https://www.youtube.com/watch?v=6Q5xqNkCk7w", 4, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Turn Off The Lights", "https://www.youtube.com/watch?v=8EJ3zbKTWQ8", 5, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Beggin'", "https://www.youtube.com/watch?v=6iD1n8H6JxQ", 5, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("More Baby", "https://www.youtube.com/watch?v=6fYw3jM5T3Q", 5, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Drugs From Amsterdam", "https://www.youtube.com/watch?v=2l7P8rG4bwY", 6, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Gimme That Bounce", "https://www.youtube.com/watch?v=Bc4t3lQ2f8Q", 6, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Metro", "https://www.youtube.com/watch?v=gmYx0dS1Y7k", 6, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Taped Up Heart", "https://www.youtube.com/watch?v=cj4A9QkJ4uA", 7, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Decisions", "https://www.youtube.com/watch?v=d3hAnAnJwyU", 7, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Sweat", "https://www.youtube.com/watch?v=4mBf8S2L7dY", 7, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Piece Of Your Heart", "https://www.youtube.com/watch?v=RhmUnk454MA", 8, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Lose Control", "https://www.youtube.com/watch?v=NAj26rVWK14", 8, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Paradise", "https://www.youtube.com/watch?v=VlM8BXylDoQ", 8, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("No Eyes", "https://www.youtube.com/watch?v=tK7Vv0yS2B4", 9, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Heartbeat", "https://www.youtube.com/watch?v=6hC5M2iQ9r4", 9, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("The Drums (Din Daa Daa)", "https://www.youtube.com/watch?v=1v2mJ0nG4nI", 9, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("17", "https://www.youtube.com/watch?v=Vn1xRrG2Y7M", 10, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Piece of Me", "https://www.youtube.com/watch?v=4z6QxNfP6dM", 10, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Always", "https://www.youtube.com/watch?v=2P4mT9sY2uQ", 10, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("(It Goes Like) Nanana", "https://www.youtube.com/watch?v=sCz5y84dwuA", 11, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Starry Night", "https://www.youtube.com/watch?v=5dJG_DdOuOM", 11, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("I Go", "https://www.youtube.com/watch?v=5qLTd8W8Y7U", 11, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Cola", "https://www.youtube.com/watch?v=qke-jOUqSXU", 12, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Panic Room", "https://www.youtube.com/watch?v=R3JtQq9tG9c", 12, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Breathe", "https://www.youtube.com/watch?v=VbQJ0hQqK4A", 12, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Slow Down", "https://www.youtube.com/watch?v=8M6J6Vg0F4I", 13, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Free", "https://www.youtube.com/watch?v=bwQ5nq6mF6k", 13, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("It Is What It Is", "https://www.youtube.com/watch?v=F4M4w7W0V0w", 13, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Latch", "https://www.youtube.com/watch?v=93ASUImTedo", 14, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("You & Me (Flume Remix)", "https://www.youtube.com/watch?v=OUkkaqSNduU", 14, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Help Me Lose My Mind", "https://www.youtube.com/watch?v=SnI4CGjeVOM", 14, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("I'm Good (Blue)", "https://www.youtube.com/watch?v=90RLzVUuXe4", 15, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("When Love Takes Over", "https://www.youtube.com/watch?v=zudbz4hOcbc", 15, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Play Hard", "https://www.youtube.com/watch?v=5dbEhBKGOtY", 15, 2))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Sugar", "https://www.youtube.com/watch?v=bvC_0foemLY", 16, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Prayer in C", "https://www.youtube.com/watch?v=fiore9Z5iUg", 16, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("In Your Eyes", "https://www.youtube.com/watch?v=1__CAdTJ5JU", 16, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Hypnotized", "https://www.youtube.com/watch?v=J5fE8xVjFvY", 17, 1))

            cursor.execute("""
            INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
            """, ("Fireworks", "https://www.youtube.com/watch?v=8x-M7AkTvrQ", 17, 1))

        # PLAYLISTS
        cursor.execute("SELECT COUNT(*) FROM playlists")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO playlists (name, genre_id) VALUES (?, ?)", ("Deep House Mix", 1))
            cursor.execute("INSERT INTO playlists (name, genre_id) VALUES (?, ?)", ("Tech House Mix", 2))
            cursor.execute("INSERT INTO playlists (name, genre_id) VALUES (?, ?)", ("Afro House Mix", 3))
            cursor.execute("INSERT INTO playlists (name, genre_id) VALUES (?, ?)", ("Progressive House Mix", 4))

        conn.commit()
        conn.close()

seed_data()

if __name__ == "__main__":
    app.run(debug=True)