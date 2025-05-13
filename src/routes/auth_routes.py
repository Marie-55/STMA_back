from flask import Blueprint
from src.controllers.auth_controller import login

auth_routes = Blueprint('/auth_routes', __name__)

auth_routes.add_url_rule('/login', view_func=login, methods=['POST'])
