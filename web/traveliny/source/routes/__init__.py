from flask import Blueprint

index_bp = Blueprint("index", __name__)
login_bp = Blueprint("login", __name__)
profile_bp = Blueprint("profile", __name__)
logout_bp = Blueprint("logout", __name__)
