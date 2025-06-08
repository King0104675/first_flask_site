import os
import sqlite3
from flask import Flask, render_template, url_for, Response, request, redirect, session

app = Flask(__name__)
app.secret_key = 'king is great'

DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, password, name))
        conn.commit()
        conn.close()
        return Response(f'''Account for {name} created successfully <br>
        <a href="{url_for('login')}">Login</a>''')
    except sqlite3.IntegrityError:
        conn.close()
        return Response(f"{username} is already taken.")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/submit1", methods=["GET", "POST"])
def submit1():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        real_name = user[0]
        session['user'] = username
        return Response(f'''Welcome {real_name}<br>
        <a href="{url_for('logout')}">Logout</a>''')
    else:
        return "Invalid Credentials. Try Again"

@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template("index.html")

port = int(os.environ.get("PORT", 5000))  # For Render or local
app.run(host="0.0.0.0", port=port)
