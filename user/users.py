from flask import Blueprint, jsonify, request, Response
from .models import User
import jwt
from flask import current_app
from flask import request, abort
from functools import wraps
from . import app
from werkzeug.security import check_password_hash

bp_user = Blueprint("users", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user= User.query.filter(id=data["user_id"]).first()
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["active"]:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated


@bp_user.route("/cox")
def home():
    return "Hello, Users!"


def get_by_email(email):
    """Get a user by email"""
    user = User.query.filter_by(mail=email).first()
    if not user:
        return
    return user

def login_real(email, password):
   print("""Login a user""")
   user = get_by_email(email)
   if not user or not check_password_hash(user.password, password):
      return
   return user

@bp_user.route("/users/login", methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True)
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        is_validated = True
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = login_real(data["email"], data["password"])
        if user:
            try:
                # token should expire after 24 hrs
                token = jwt.encode(
                    {"user_id": user.id},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "token": token
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500