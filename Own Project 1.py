import os
from flask import Flask, render_template, url_for, Response, request, redirect, session

app = Flask(__name__)
app.secret_key = 'king is great'

website_users={}

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
    if username in website_users:
        return Response(f"{username} is already taken.")
    else:
        website_users[username] = [password, name]
        return Response(f'''Account for {name} created successfully <br>
        <a href={url_for('login')}>Login</a>
        ''')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/submit1", methods=["GET", "POST"])
def submit1():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in website_users and website_users[username][0] == password:
        real_name = website_users[username][1]
        session['user']=username
        return Response(f'''Welcome {real_name}<br>
        <a href="{url_for('logout')}">Logout</a>
        ''')
    else:
        return "Invalid Credentials. Try Again"

@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template('index.html')


port = int(os.environ.get("PORT", 5000))  # Render will set PORT env variable
app.run(host="0.0.0.0", port=port)

