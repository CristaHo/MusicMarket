from app import app
from flask import render_template, request, redirect, session
from db import db
from os import getenv
import users
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

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
## user_id mukaan kaikkien biisien hakuun
## tee myös genrejuttu
## sit 
def search(): 
    sql_all_songs = text("SELECT tracks.id, tracks.artist, tracks.track, tracks.genre, tracks.price FROM tracks LEFT JOIN users ON tracks.artist=users.username")
    sql_all_songs1 = db.session.execute(sql_all_songs).fetchall()
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
    get_id = result.fetchone()
    user_id = get_id[0]
    sql = text("SELECT DISTINCT tracks.id, COALESCE(likes.id, 0), tracks.artist, tracks.track FROM tracks LEFT JOIN tracks_bought ON tracks.id=tracks_bought.track_id LEFT JOIN likes ON tracks.id=likes.track_id WHERE tracks_bought.user_id = :user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    results = result.fetchall()
    return render_template("search.html", results=results, sql_all_songs1=sql_all_songs1)

@app.route("/search_result", methods=["GET"])
def search_result():
    chooseone = request.args["chooseone"]
    searchword = request.args["searchword"]

    if chooseone == "1":
        sql = text("SELECT id, artist, track FROM tracks WHERE artist LIKE :searchword")
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
        return render_template("search_result.html", results=results)
    
    elif chooseone == "2":
        sql = text("SELECT id, artist, track FROM tracks WHERE track LIKE :searchword")
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
        return render_template("search_result.html", results=results)

    elif chooseone == "3":
        sql = text("SELECT id, artist, track FROM tracks WHERE genre LIKE :searchword")
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
        return render_template("search_result.html", results=results)

    ## Testaa tää
    elif chooseone == "":
        message = "You must choose a search category"
        return render_template("error.html", message=message)
    

@app.route("/buy_song", methods=["POST"])
def buy_song():
    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
    get_id = result.fetchone()
    user_id = get_id[0]
    sql_track = text("SELECT artist, track FROM tracks WHERE tracks.id = :track_id")
    sql_track_result = db.session.execute(sql_track, {"track_id":track_id})
    get_track = sql_track_result.fetchone()
    artist = get_track[0]
    track = get_track[1]


    sql = text("INSERT INTO tracks_bought (user_id, track_id) VALUES (:user_id, :track_id)")
    db.session.execute(sql, {"user_id":user_id, "track_id":track_id})
    db.session.commit()
    return render_template("track_bought.html", artist=artist, track=track)



@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        username = session["username"]
        sql = text("SELECT track, genre FROM tracks WHERE artist LIKE :username")
        result = db.session.execute(sql, {"username":username})
        results = result.fetchall()
        sql2 = text("SELECT SUM(price) FROM tracks INNER JOIN tracks_bought ON tracks.id=tracks_bought.track_id WHERE artist LIKE :username")
        result2 = db.session.execute(sql2, {"username":username})
        bought = result2.fetchone()[0]
        return render_template("upload.html", results=results, bought=bought)
    if request.method == "POST":
        artist = session["username"]
        trackname = request.form["songname"]
        genre = request.form["genre"]
        price = request.form["price"]
        sql = text("INSERT INTO tracks (artist, track, genre, price, date) VALUES (:artist, :track, :genre, :price, NOW())")
        db.session.execute(sql, {"artist":artist, "track":trackname, "genre":genre, "price":price})
        db.session.commit()
        return redirect("/")

@app.route("/like", methods=["POST"])
def like():
    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
    get_id = result.fetchone()
    user_id = get_id[0]

    sql_like = text("INSERT INTO likes (user_id, track_id) VALUES (:user_id, :track_id)")
    db.session.execute(sql_like, {"user_id":user_id, "track_id":track_id})
    db.session.commit()
    return redirect("/")

@app.route("/comment", methods=["POST"])
def comment():
    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
    get_id = result.fetchone()
    user_id = get_id[0]
    comment = request.form["comment"]

    sql_like = text("INSERT INTO comments (user_id, track_id, comment) VALUES (:user_id, :track_id, :comment)")
    db.session.execute(sql_like, {"user_id":user_id, "track_id":track_id, "comment":comment})
    db.session.commit()
    return render_template("comment.html")

@app.route("/track/<int:track_id>")
def track(track_id):
    sql = db.session.execute(text("SELECT artist, track FROM tracks WHERE id = :track_id"), {"track_id":track_id}).fetchone()
    artist = sql[0]
    track = sql[1]
    likes = db.session.execute(text("SELECT COUNT(id) FROM likes WHERE likes.track_id = :track_id"), {"track_id":track_id}).fetchone()[0]
    comments = db.session.execute(text("SELECT comments.comment, users.username FROM comments INNER JOIN users ON comments.user_id=users.id WHERE comments.track_id = :track_id"), {"track_id":track_id}).fetchall()
    return render_template("track.html", artist=artist, track=track, likes=likes, comments=comments)

@app.route("/artist/<int:user_id>")
def artist(user_id):
    sql = db.session.execute(text("SELECT track, genre FROM tracks WHERE artist = :user_id"), {"user_id":user_id}).fetchall()
    
    ##likes = db.session.execute(text("SELECT COUNT(id) FROM likes WHERE likes.track_id = :track_id"), {"track_id":track_id}).fetchone()[0]
    ##comments = db.session.execute(text("SELECT comment FROM comments WHERE comments.track_id = :track_id"), {"track_id":track_id}).fetchall()
    return render_template("artist.html", sql=sql)