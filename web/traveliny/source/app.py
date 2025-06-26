import os
from flask import Flask
from routes.index import index_bp
from routes.login import login_bp
from routes.profile import profile_bp
from routes.logout import logout_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(index_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(logout_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
