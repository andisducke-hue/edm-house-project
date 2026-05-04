from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/genres")
def genres():
    return render_template("genres.html")

if __name__ == "__main__":
    app.run(debug=True)