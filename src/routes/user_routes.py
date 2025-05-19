from flask import Blueprint, request, jsonify
import src.controllers.user_controller  as user 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.firebase.user_model import FirebaseUser
from src.utils.firebase_utils import verify_token
from src.utils.db_factory import DatabaseFactory
from src.utils.util_func import model_to_dict


user_routes=Blueprint("/user",__name__)

@user_routes.route("/sign_up",methods=['POST'])
def signup():
    """ hello my name is user here is my group project project , as a first year student i realluy hate ensia bzf , but it is good y3ni , still """
    
    data = request.get_json()
    email = data.get("email")
    password = data.get("password").strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    existing_user = user.get_user(email)
    print(existing_user)
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    hashed_password = str(generate_password_hash(password))
    print(f"password hash length is : {len(hashed_password)}")
    print(f"password hash  : {(hashed_password)}")

    
    print(f"the check is: {check_password_hash(hashed_password,password=password)}")
    new_user = user.create_user(email=email, password=hashed_password)

    return jsonify({"message": "User registered successfully", "email": new_user.email}), 200


#auth_routes.add_url_rule('/login', view_func=login, methods=['POST'])
@user_routes.route("/login",methods=['POST'])
def login():
        data = request.get_json()
        email = data.get("email")
        password = str(data.get("password").strip())

        if not email or not password:
            return {"error": "missing_fields", "message": "Email and password are required"}
            
        #user_model = DatabaseFactory.get_user_model()

        user_ = user.get_user(email)
        
        # Check if user exists
        if user_==None:
            return {"error": "user_not_found", "message": "No account found with this email"},404
        
        # Check if password matches
        check_pass=str(user.get_user_password(email))
        print(f"password hash length is : {len(check_pass)}")
        print(f"password is {password}")
        print(f"password hash is {check_pass}")
        print(check_password_hash(check_pass,password=password))
        print(type(check_pass)) 

        if not check_password_hash(check_pass,password=password):
            return {"error": "invalid_password", "message": "Incorrect password"},405
        user_=model_to_dict(user_)
            
        return {"success": True, "user": user_},200


# # Login Route
# @user_routes.route("/login", methods=["POST"])
# def login_route():
#     data = request.json
#     log=logIn(data.get('email'), data.get('password'))
#     if log:
#         return jsonify({"message":"user logged in"}) ,200
#     else:
#         return jsonify({"message":"user cannot be logged in"}) ,404


# # Authentication Check Route
# @user_routes.route("/check-auth", methods=["GET"])
# def check_auth_route():
#     check=check_user_authen()
#     if check:
#         return jsonify({"message":"user checked"}) ,200
#     else:
#         return jsonify({"message":"user cannot be checked"}) ,404


# # Logout Route
# @user_routes.route("/logout", methods=["POST"])
# def logout_route():
#     logout=log_out()
#     check_user_authen
#     if check:
#         return jsonify({"message": "Logged out"}) ,200
#     else:
#         return jsonify({"message":"user cannot be logged out"}) ,404


