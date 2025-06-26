from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3 
import os
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  
app.config['DATABASE'] = os.path.join(app.root_path, 'aeroserve.db')
ADMIN_OTP = None

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["1000 per hour"], 
    storage_uri="memory://"
)

FLAG = os.getenv("FLAG", "METACTF{this_is_a_fake_flag}")

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        otp TEXT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def create_admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, phone_number) VALUES (?, ?, ?)", 
                     ('admin', secrets.token_hex(16), '1234567890'))
        conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute") 
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        phone_number = request.form.get("phone_number")

        # Validate phone number
        if not phone_number.isdigit() or len(phone_number) != 10:
            return render_template("register.html", error="Invalid phone number. Please enter a 10-digit number.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template("register.html", error="Username already exists")

        cursor.execute("INSERT INTO users (username, password, phone_number) VALUES (?, ?, ?)", 
                     (username, password, phone_number))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        otp = f"{random.randint(0, 99999999):08}"
        cursor.execute("UPDATE users SET otp = ? WHERE username = ?", (otp, username))
        conn.commit()
        session["user"] = username
        cursor.close()
        conn.close()
        
        if username == "admin":
            global ADMIN_OTP
            ADMIN_OTP = otp
            return jsonify({"otp": "OTP Sent to admin's phone number"})
        return jsonify({"otp": otp})
    else:
        cursor.close()
        conn.close()
        return jsonify({"error": "Invalid username"}), 400

@app.route("/verify_otp", methods=["POST"])
@limiter.limit("3 per minute")
def verify_otp():
    otp = str(request.form.get("otp"))
    username = session.get("user", "").lower()
    if not username:
        return render_template("login.html", error="Session expired. Please log in again.")

    if username == "admin" and otp == ADMIN_OTP:
        session["autheticated"] = True
        return redirect(url_for("home"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT otp FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    stored_otp = result[0] if result else None

    if stored_otp and stored_otp == otp:
        cursor.execute("UPDATE users SET otp = NULL WHERE username = ?", (username,))
        conn.commit()
        cursor.close()
        conn.close()
        session["autheticated"] = True
        return redirect(url_for("home"))
    else:
        cursor.close()
        conn.close()
        return jsonify({"error": "Invalid OTP"}), 400

@app.route("/home")
def home():
    if session.get("autheticated") == True:
        if session.get("user") == "admin":
            message = f"Admin, your flag is: {FLAG}"
            return render_template("home.html", user=message)
        else:
            return render_template("home.html", user=session.get("user"))
    return redirect(url_for("login"))

# Simple action handlers that only update session
@app.route("/maintenance_action", methods=["POST"])
def maintenance_action():
    if not session.get("autheticated"):
        return redirect(url_for("login"))
    
    aircraft = request.form.get("aircraft")
    maintenance_type = request.form.get("maintenance_type")
    
    session["last_action"] = f"Scheduled {maintenance_type} for {aircraft}"
    session["maintenance_count"] = session.get("maintenance_count", 0) + 1
    
    return redirect(url_for("home"))

@app.route("/refuel_action", methods=["POST"])
def refuel_action():
    if not session.get("autheticated"):
        return redirect(url_for("login"))
    
    aircraft = request.form.get("aircraft")
    fuel_amount = request.form.get("fuel_amount")
    
    session["last_action"] = f"Added {fuel_amount} gallons to {aircraft}"
    session["refuel_count"] = session.get("refuel_count", 0) + 1
    
    return redirect(url_for("home"))

@app.route("/inspection_action", methods=["POST"])
def inspection_action():
    if not session.get("autheticated"):
        return redirect(url_for("login"))
    
    aircraft = request.form.get("aircraft")
    inspection_type = request.form.get("inspection_type")
    
    session["last_action"] = f"Scheduled {inspection_type} for {aircraft}"
    session["inspection_count"] = session.get("inspection_count", 0) + 1
    
    return redirect(url_for("home"))

@app.route("/flight_plan_action", methods=["POST"])
def flight_plan_action():
    if not session.get("autheticated"):
        return redirect(url_for("login"))
    
    aircraft = request.form.get("aircraft")
    destination = request.form.get("destination")
    
    session["last_action"] = f"Created flight plan for {aircraft} to {destination}"
    session["flight_plan_count"] = session.get("flight_plan_count", 0) + 1
    
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'js'), filename)

@app.route('/lib/<path:filename>')
def serve_lib(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'lib'), filename)

@app.route('/scss/<path:filename>')
def serve_scss(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'scss'), filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), filename)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": f"You have exceeded the rate limit. Please try again in {e.retry_after} seconds."
    }), 429

if __name__ == "__main__":
    init_db()
    create_admin()
    app.run("0.0.0.0", port=1337, debug=False)