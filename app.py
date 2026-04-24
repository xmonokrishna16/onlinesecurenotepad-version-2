import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Remember to change this secret key to a random string before sharing your website!
app.secret_key = "secure_notepad_secret"

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=os.environ.get("DB_PORT")
    )

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                           (username, password))
            db.commit()
            cursor.close()
            db.close()
            return redirect("/login")
        except mysql.connector.IntegrityError:
            return "Username already exists!"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        # user is a tuple: (id, username, password)
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            return "Invalid Credentials!"

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        note = request.form["note"]
        cursor.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s)",
                   (user_id, note))
        db.commit()

    # Fetch notes using %s
    cursor.execute("SELECT * FROM notes WHERE user_id=%s", (user_id,))
    notes = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template("dashboard.html", notes=notes)

@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM notes WHERE id=%s", (id,))
        db.commit()
        cursor.close()
        db.close()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)