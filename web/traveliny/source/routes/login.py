from flask import Blueprint, request, render_template, redirect, url_for, session
from db import get_db_connection

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        Safe_sql =['SELECT','UPDATE','UNION','DELETE','INSERT','CREATE','DROP','ALTER','RENAME','GRANT','REVOKE','SET','SHOW','DESCRIBE','EXPLAIN']
        if any(word in username for word in Safe_sql) or any(word in password for word in Safe_sql):
            return render_template("login.html", error="Invalid input detected. Please try again.")
        conn = get_db_connection()
        if not conn:
            return render_template("login.html", error="Database connection failed.")
        
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(query)
        user = None

        try:
            cursor.execute(query)
            
            user = cursor.fetchone()
            
            while cursor.fetchone() is not None:
                pass

            while cursor.nextset():
                while cursor.fetchone() is not None:
                    pass
                    
        except Exception as err:
            print(f"Database error: {err}")
            return render_template("login.html", error="An error occurred during login.")
        finally:
            cursor.close()
            conn.close()

        if user:
            session["user"] = user[1]  
            return redirect(url_for("profile.profile"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")