from app import app
from flask import render_template, request, redirect, session
from db import db
from os import getenv
import users
from flask_sqlalchemy import SQLAlchemy

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        return redirect("/")
    
    else:
        return render_template("error.html", message="Väärä tunnus")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", register=False)
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        else:
            if users.register(username, password1):
                return render_template("register.html", register=True)
            
            else:
                return render_template("error.html", message="Käyttäjän lisääminen ei onnistunut")
       
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/search", methods=["GET"])
def search():
    username = session["username"]
    sql_user_id = "SELECT id FROM users WHERE username LIKE :username"
    result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
    get_id = result.fetchone()
    user_id = get_id[0]
    sql = "SELECT tracks.artist, tracks.track FROM tracks LEFT JOIN tracks_bought ON tracks.id=tracks_bought.track_id WHERE tracks_bought.user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    results = result.fetchall()
    return render_template("search.html", results=results)

@app.route("/search_result", methods=["GET"])
def search_result():
    chooseone = request.args["chooseone"]
    searchword = request.args["searchword"]

    if chooseone == "1":
        sql = "SELECT id, artist, track FROM tracks WHERE artist LIKE :searchword"
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
    
    elif chooseone == "2":
        sql = "SELECT id, artist, track FROM tracks WHERE track LIKE :searchword"
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()

    elif chooseone == "3":
        sql = "SELECT id, artist, track FROM tracks WHERE genre LIKE :searchword"
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
    return render_template("search_result.html", results=results)

@app.route("/buy_song", methods=["POST"])
def buy_song():
    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = "SELECT id FROM users WHERE username LIKE :username"
    result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
    get_id = result.fetchone()
    user_id = get_id[0]


    sql = "INSERT INTO tracks_bought (user_id, track_id) VALUES (:user_id, :track_id)"
    db.session.execute(sql, {"user_id":user_id, "track_id":track_id})
    db.session.commit()
    return redirect("/")



@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        username = session["username"]
        sql = "SELECT track, genre FROM tracks WHERE artist LIKE :username"
        result = db.session.execute(sql, {"username":username})
        results = result.fetchall()
        sql2 = "SELECT COUNT(tracks_bought.id) FROM tracks_bought LEFT JOIN tracks ON tracks_bought.track_id = tracks.id WHERE tracks.artist LIKE :username"
        result2 = db.session.execute(sql2, {"username":username})
        bought = result2.fetchone()[0]
        return render_template("upload.html", results=results, bought=bought)
    if request.method == "POST":
        artist = session["username"]
        trackname = request.form["songname"]
        genre = request.form["genre"]
        sql = "INSERT INTO tracks (artist, track, genre, date) VALUES (:artist, :track, :genre, NOW())"
        db.session.execute(sql, {"artist":artist, "track":trackname, "genre":genre})
        db.session.commit()
        return redirect("/")
