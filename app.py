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
        image = request.form["image"]
        about = request.form["about"]

        cursor.execute("""
        UPDATE artists
        SET name=?, image=?, about=?
        WHERE id=?
        """, (name, image, about, id))

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

    # =========================
    # GENRES
    # =========================

    cursor.execute("SELECT COUNT(*) FROM genres")

    if cursor.fetchone()[0] == 0:

        genres = [

            ("Chicago House", "The original house style from Chicago, built on drum machines and dance grooves."),
            ("Acid House", "Hypnotic house music with iconic TB-303 acid basslines."),
            ("Deep House", "Smooth and soulful house music with deep bass and atmospheric vibes."),
            ("Progressive House", "Melodic festival-oriented house music with emotional builds."),
            ("French House", "Disco-inspired filtered house music from France."),
            ("Funky House", "Groovy and disco-inspired upbeat house music."),
            ("Tribal House", "Percussion-heavy house with tribal rhythm influences."),
            ("Afro House", "African-inspired deep rhythmic house music."),
            ("Tropical House", "Relaxed melodic summer-style house music."),
            ("Electro House", "Aggressive electronic house with strong drops and synths."),
            ("Bass House", "Bass-focused energetic modern house music."),
            ("Slap House", "Modern commercial house with bouncing basslines."),
            ("Future House", "Modern house with bright synths and future-style grooves."),
            ("Garage House", "UK garage influenced vocal house music."),
            ("Lo-Fi House", "Raw nostalgic underground house music."),
            ("Minimal House", "Minimalistic repetitive stripped-down house grooves."),
            ("Latin House", "House music blended with Latin rhythms.")

        ]

        cursor.executemany(
            "INSERT INTO genres (name, description) VALUES (?, ?)",
            genres
        )

    # =========================
    # ARTISTS
    # =========================

    cursor.execute("SELECT COUNT(*) FROM artists")

    if cursor.fetchone()[0] == 0:

        artists = [

            ("Fred again..", "/static/artist_images/fred-again.jpg",
             "UK electronic producer blending emotional vocals with house and garage."),

            ("FISHER", "/static/artist_images/fisher.jpg",
             "Australian tech house DJ known for energetic festival records."),

            ("John Summit", "/static/artist_images/john-summit.jpg",
             "American producer combining tech house with festival energy."),

            ("Dom Dolla", "/static/artist_images/dom-dolla.jpg",
             "Australian house producer recognized for groovy club tracks."),

            ("Chris Lake", "/static/artist_images/chris-lake.jpg",
             "British producer famous for groove-driven tech house."),

            ("Mau P", "/static/artist_images/mau-p.jpg",
             "Dutch DJ producing modern underground tech house."),

            ("KREAM", "/static/artist_images/kream.jpg",
             "Norwegian duo making melodic deep house music."),

            ("MEDUZA", "/static/artist_images/meduza.jpg",
             "Italian trio known for emotional deep house crossover hits."),

            ("Claptone", "/static/artist_images/claptone.jpg",
             "Mysterious house DJ with melodic deep house style."),

            ("MK", "/static/artist_images/mk.jpg",
             "Legendary American house producer and deep house pioneer."),

            ("Peggy Gou", "/static/artist_images/peggy-gou.jpg",
             "South Korean DJ blending house and underground electronic sounds."),

            ("CamelPhat", "/static/artist_images/camelphat.jpg",
             "British duo producing melodic progressive house."),

            ("Vintage Culture", "/static/artist_images/vintage-culture.jpg",
             "Brazilian DJ blending melodic and deep house styles."),

            ("Disclosure", "/static/artist_images/disclosure.jpg",
             "British electronic duo mixing garage and house music."),

            ("David Guetta", "/static/artist_images/david-guetta.jpg",
             "Global EDM producer combining house and pop music."),

            ("Robin Schulz", "/static/artist_images/robin-schulz.jpg",
             "German producer famous for melodic tropical house."),

            ("Purple Disco Machine", "/static/artist_images/purple-disco-machine.jpg",
             "Disco-inspired funky house producer from Germany."),

            ("Gorgon City", "/static/artist_images/gorgon-city.jpg",
             "UK duo blending deep house and garage."),

            ("Ben Hemsley", "/static/artist_images/ben-hemsley.jpg",
             "British rave-inspired house producer."),

            ("Jamie Jones", "/static/artist_images/jamie-jones.jpg",
             "Influential underground house and tech house DJ."),

            ("Alan Walker", "/static/artist_images/alan-walker.jpg",
             "Norwegian electronic producer known for melodic EDM."),

            ("Kygo", "/static/artist_images/kygo.jpg",
             "Producer who popularized tropical house globally."),

            ("Avicii", "/static/artist_images/avicii.jpg",
             "Legendary Swedish progressive house producer."),

            ("Alesso", "/static/artist_images/alesso.jpg",
             "Swedish producer famous for progressive house anthems."),

            ("Calvin Harris", "/static/artist_images/calvin-harris.jpg",
             "Scottish producer combining dance and funk influences."),

            ("TheFatRat", "/static/artist_images/thefatrat.jpg",
             "Electronic producer known for melodic EDM and gaming music."),

            ("Tobu", "/static/artist_images/tobu.jpg",
             "Latvian melodic progressive house producer."),

            ("Vicetone", "/static/artist_images/vicetone.jpg",
             "Dutch duo making energetic progressive house."),

            ("Swedish House Mafia", "/static/artist_images/swedish-house-mafia.jpg",
             "Legendary Swedish progressive house trio."),

            ("Kaskade", "/static/artist_images/kaskade.jpg",
             "American deep and melodic house producer."),

            ("Black Coffee", "/static/artist_images/black-coffee.jpg",
             "South African Afro house pioneer."),

            ("Tchami", "/static/artist_images/tchami.jpg",
             "French future house producer."),

            ("Oliver Heldens", "/static/artist_images/oliver-heldens.jpg",
             "Dutch future house DJ and producer."),

            ("Daft Punk", "/static/artist_images/daft-punk.jpg",
             "Iconic French electronic music duo."),

            ("Lane 8", "/static/artist_images/lane8.jpg",
             "Melodic deep and progressive house producer."),

            ("Riton", "/static/artist_images/riton.jpg",
             "British electronic producer known for dance crossover tracks.")

        ]

        cursor.executemany(
            "INSERT INTO artists (name, image, about) VALUES (?, ?, ?)",
            artists
        )

    # =========================
    # CREATE MAPS
    # =========================

    cursor.execute("SELECT id, name FROM artists")
    artist_map = {name: id for id, name in cursor.fetchall()}

    cursor.execute("SELECT id, name FROM genres")
    genre_map = {name: id for id, name in cursor.fetchall()}

    # =========================
    # TRACKS
    # =========================

    cursor.execute("SELECT COUNT(*) FROM tracks")

    if cursor.fetchone()[0] == 0:

        tracks = [

            # DEEP HOUSE
            ("Piece Of Your Heart", "https://www.youtube.com/watch?v=KWjV25q34Hw", "MEDUZA", "Deep House"),
            ("Lose Control", "https://www.youtube.com/watch?v=-3P2USPFDcE", "MEDUZA", "Deep House"),
            ("Cola", "https://www.youtube.com/watch?v=qke-jOUqSXU", "CamelPhat", "Deep House"),
            ("No Eyes", "https://www.youtube.com/watch?v=CXyVMvlS1NU", "Claptone", "Deep House"),
            ("Taped Up Heart", "https://www.youtube.com/watch?v=1hhSxCme8EI", "KREAM", "Deep House"),

            # PROGRESSIVE HOUSE
            ("Wake Me Up", "https://www.youtube.com/watch?v=IcrbM1l_BoI", "Avicii", "Progressive House"),
            ("Levels", "https://www.youtube.com/watch?v=_ovdm2yX4MA", "Avicii", "Progressive House"),
            ("Heroes", "https://www.youtube.com/watch?v=a7SouU3ECpU", "Alesso", "Progressive House"),
            ("Under Control", "https://www.youtube.com/watch?v=yZqmarGShxg", "Alesso", "Progressive House"),
            ("Calling", "https://www.youtube.com/watch?v=9G1I16gJBvU", "Swedish House Mafia", "Progressive House"),

            # TROPICAL HOUSE
            ("Firestone", "https://www.youtube.com/watch?v=9Sc-ir2UwGU", "Kygo", "Tropical House"),
            ("Stole The Show", "https://www.youtube.com/watch?v=BgfcToAjfdc", "Kygo", "Tropical House"),
            ("It Ain't Me", "https://www.youtube.com/watch?v=u3VTKvdAuIY", "Kygo", "Tropical House"),
            ("Sugar", "https://www.youtube.com/watch?v=bvC_0foemLY", "Robin Schulz", "Tropical House"),
            ("Prayer in C", "https://www.youtube.com/watch?v=fiore9Z5iUg", "Robin Schulz", "Tropical House"),

            # FUTURE HOUSE
            ("Gecko", "https://www.youtube.com/watch?v=jjx2oc2NRzA", "Oliver Heldens", "Future House"),
            ("Turn Me On", "https://www.youtube.com/watch?v=ng3XUABcwDw", "Riton", "Future House"),
            ("Saving Up", "https://www.youtube.com/watch?v=yAl6yiQHHNw", "Dom Dolla", "Future House"),
            ("More Baby", "https://www.youtube.com/watch?v=KxZ_W9zX8ho", "Chris Lake", "Future House"),
            ("Piece of Me", "https://www.youtube.com/watch?v=3HCtJ5m96YE", "MK", "Future House"),

            # BASS HOUSE
            ("Losing It", "https://www.youtube.com/watch?v=o3WdLtpWM_c", "FISHER", "Bass House"),
            ("You Little Beauty", "https://www.youtube.com/watch?v=X4xF5ymdQG8", "FISHER", "Bass House"),
            ("Atmosphere", "https://www.youtube.com/watch?v=MlwBZ2MSNtE", "FISHER", "Bass House"),
            ("Turn Off The Lights", "https://www.youtube.com/watch?v=E_wxPpRSgho", "Chris Lake", "Bass House"),
            ("Beggin", "https://www.youtube.com/watch?v=x8mdqMcOAUo", "Chris Lake", "Bass House"),

            # SLAP HOUSE
            ("Head & Heart", "https://www.youtube.com/watch?v=CRuOOxF-ENQ", "Joel Corry", "Slap House"),
            ("Breaking Me", "https://www.youtube.com/watch?v=jIoEaTN7GGo", "Riton", "Slap House"),
            ("Paradise", "https://www.youtube.com/watch?v=e7HBypw4lhY", "MEDUZA", "Slap House"),
            ("In Your Eyes", "https://www.youtube.com/watch?v=mDLiAs5k1oI", "Robin Schulz", "Slap House"),
            ("The Business", "https://www.youtube.com/watch?v=nCg3ufihKyU", "Tiësto", "Slap House"),

            # GARAGE HOUSE
            ("Latch", "https://www.youtube.com/watch?v=93ASUImTedo", "Disclosure", "Garage House"),
            ("White Noise", "https://www.youtube.com/watch?v=bkk2H3Ztrfk", "Disclosure", "Garage House"),
            ("Omen", "https://www.youtube.com/watch?v=fB63ztKnGvo", "Disclosure", "Garage House"),
            ("Help Me Lose My Mind", "https://www.youtube.com/watch?v=XJY66qPDeeQ", "Disclosure", "Garage House"),
            ("You & Me", "https://www.youtube.com/watch?v=OUkkaqSNduU", "Disclosure", "Garage House"),

            # AFRO HOUSE
            ("Drive", "https://www.youtube.com/watch?v=32HANv-bdJs", "Black Coffee", "Afro House"),
            ("Your Eyes", "https://www.youtube.com/watch?v=PPUyHWWrQzE", "Black Coffee", "Afro House"),
            ("Slow Down", "https://www.youtube.com/watch?v=76mkEfxxIl0", "Vintage Culture", "Afro House"),
            ("Free", "https://www.youtube.com/watch?v=2_a2ZUOJiMs", "Vintage Culture", "Afro House"),
            ("Human", "https://www.youtube.com/watch?v=6mn7OonJfk4", "John Summit", "Afro House"),

            # ELECTRO HOUSE
            ("Titanium", "https://www.youtube.com/watch?v=JRfuAukYTKg", "David Guetta", "Electro House"),
            ("Animals", "https://www.youtube.com/watch?v=gCYcHz2k5x0", "Martin Garrix", "Electro House"),
            ("Booyah", "https://www.youtube.com/watch?v=QCyIY10KBnk", "Showtek", "Electro House"),
            ("Tsunami", "https://www.youtube.com/watch?v=0EWbonj7f18", "DVBBS", "Electro House"),
            ("Play Hard", "https://www.youtube.com/watch?v=5dbEhBKGOtY", "David Guetta", "Electro House")

        ]

        for title, link, artist_name, genre_name in tracks:

            if artist_name not in artist_map:
                continue

            if genre_name not in genre_map:
                continue

            cursor.execute(
                """
                INSERT INTO tracks (title, youtube_link, artist_id, genre_id)
                VALUES (?, ?, ?, ?)
                """,
                (
                    title,
                    link,
                    artist_map[artist_name],
                    genre_map[genre_name]
                )
            )

    # =========================
    # PLAYLISTS
    # =========================

    cursor.execute("SELECT COUNT(*) FROM playlists")

    if cursor.fetchone()[0] == 0:

        playlists = [

            ("Deep House Vibes", "Deep House"),
            ("Progressive House Festival", "Progressive House"),
            ("Tropical Summer", "Tropical House"),
            ("Future House Energy", "Future House"),
            ("Bass House Madness", "Bass House"),
            ("Garage House Essentials", "Garage House"),
            ("Afro House Sunset", "Afro House"),
            ("Electro House Anthems", "Electro House")

        ]

        for playlist_name, genre_name in playlists:

            cursor.execute(
                "INSERT INTO playlists (name, genre_id) VALUES (?, ?)",
                (
                    playlist_name,
                    genre_map[genre_name]
                )
            )

    conn.commit()
    conn.close()


seed_data()

if __name__ == "__main__":
    app.run(debug=True)