from os import getenv
import secrets
from sqlalchemy.sql import text
from app import app
from flask import render_template, request, redirect, session
from db import db
import users
from flask_sqlalchemy import SQLAlchemy



app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    return render_template("error.html", message="Wrong username")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", register=False)
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords don't match")
        else:
            if users.register(username, password1):
                return render_template("register.html", register=True)
            else:
                return render_template("error.html", \
                message="There was an error registering a new account")

@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
        return redirect("/")
    return redirect("/")

@app.route("/search", methods=["GET"])
def search():
    if "username" in session:
        sql_all_songs = text("SELECT tracks.id, tracks.artist, tracks.track, "\
            "tracks.genre, tracks.price " \
            "FROM tracks LEFT JOIN users ON tracks.artist=users.username")
        sql_all_songs1 = db.session.execute(sql_all_songs).fetchall()
        username = session["username"]
        sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
        result = db.session.execute(sql_user_id, {"username":"%"+username+"%"})
        get_id = result.fetchone()
        user_id = get_id[0]
        sql = text("SELECT tracks.id, tracks.artist, tracks.track, COALESCE(l.track_id, 0) " \
            "FROM tracks LEFT JOIN (SELECT likes.track_id, likes.user_id FROM likes " \
            "WHERE likes.user_id= :user_id) AS l  ON tracks.id=l.track_id " \
            "JOIN tracks_bought ON tracks.id=tracks_bought.track_id " \
            "WHERE tracks_bought.user_id= :user_id")
        result = db.session.execute(sql, {"user_id":user_id})
        results = result.fetchall()
        return render_template("search.html", results=results, sql_all_songs1=sql_all_songs1, \
            user_id=user_id, username=username)
    return render_template("error.html", message="You have to login or register first")

@app.route("/search_result", methods=["GET"])
def search_result():
    chooseone = request.args["chooseone"]
    searchword = request.args["searchword"]

    if chooseone == "1":
        sql = text("SELECT id, artist, track, genre, price FROM tracks " \
            "WHERE artist LIKE :searchword")
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
        return render_template("search_result.html", results=results)
    elif chooseone == "2":
        sql = text("SELECT id, artist, track, genre, price FROM tracks " \
            "WHERE track LIKE :searchword")
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
        return render_template("search_result.html", results=results)
    elif chooseone == "3":
        sql = text("SELECT id, artist, track, genre, price FROM tracks "\
            "WHERE genre LIKE :searchword")
        result = db.session.execute(sql, {"searchword":"%"+searchword+"%"})
        results = result.fetchall()
        return render_template("search_result.html", results=results)

@app.route("/buy_song", methods=["POST"])
def buy_song():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":username})
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
    if "username" in session:
        if request.method == "GET":
            username = session["username"]
            sql = text("SELECT id, track, genre FROM tracks WHERE artist LIKE :username")
            result = db.session.execute(sql, {"username":username})
            results = result.fetchall()
            sql2 = text("SELECT SUM(price) FROM tracks INNER JOIN tracks_bought " \
                "ON tracks.id=tracks_bought.track_id WHERE artist LIKE :username")
            result2 = db.session.execute(sql2, {"username":username})
            bought = result2.fetchone()[0]
            return render_template("upload.html", results=results, bought=bought)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            artist = session["username"]
            trackname = request.form["songname"]
            genre = request.form["genre"]
            price = request.form["price"]
            sql = text("INSERT INTO tracks (artist, track, genre, price) " \
                "VALUES (:artist, :track, :genre, :price)")
            db.session.execute(sql, {"artist":artist, "track":trackname, \
                "genre":genre, "price":price})
            db.session.commit()
            return render_template("uploaded.html")
    return render_template("error.html", message="You have to login or register first")

@app.route("/like", methods=["POST"])
def like():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":username})
    get_id = result.fetchone()
    user_id = get_id[0]

    sql_like = text("INSERT INTO likes (user_id, track_id) VALUES (:user_id, :track_id)")
    db.session.execute(sql_like, {"user_id":user_id, "track_id":track_id})
    db.session.commit()

    sql_track = text("SELECT artist, track FROM tracks WHERE id= :track_id")
    result = db.session.execute(sql_track, {"track_id":track_id})
    the_track = result.fetchone()
    artist = the_track[0]
    track = the_track[1]
    return render_template("liked.html", artist=artist, track=track)

@app.route("/comment", methods=["POST"])
def comment():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    track_id = request.form["id"]
    username = session["username"]
    sql_user_id = text("SELECT id FROM users WHERE username LIKE :username")
    result = db.session.execute(sql_user_id, {"username":username})
    get_id = result.fetchone()
    user_id = get_id[0]
    comment = request.form["comment"]

    sql_like = text("INSERT INTO comments (user_id, track_id, comment) " \
        "VALUES (:user_id, :track_id, :comment)")
    db.session.execute(sql_like, {"user_id":user_id, "track_id":track_id, "comment":comment})
    db.session.commit()
    return render_template("comment.html")

@app.route("/track/<int:track_id>")
def track(track_id):
    sql = db.session.execute(text("SELECT artist, track FROM tracks " \
        "WHERE id = :track_id"), {"track_id":track_id}).fetchone()
    artist = sql[0]
    track = sql[1]
    likes = db.session.execute(text("SELECT COUNT(id) FROM likes " \
        "WHERE likes.track_id = :track_id"), {"track_id":track_id}).fetchone()[0]
    comments = db.session.execute(text("SELECT comments.comment, users.username " \
        "FROM comments INNER JOIN users ON comments.user_id=users.id " \
        "WHERE comments.track_id = :track_id"), {"track_id":track_id}).fetchall()
    return render_template("track.html", artist=artist, track=track, likes=likes, comments=comments)
    