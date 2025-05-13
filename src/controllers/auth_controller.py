from flask import request, jsonify
from src.services.auth_service import AuthService

def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"success": False, "error": "missing_fields", "message": "Email and password required"}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    result = AuthService.login(email, password)
    
    if "error" in result:
        # Different status codes based on error type
        if result["error"] == "user_not_found":
            return jsonify({"success": False, "error": result["error"], "message": result["message"]}), 404
        elif result["error"] == "invalid_password":
            return jsonify({"success": False, "error": result["error"], "message": result["message"]}), 401
        else:
            return jsonify({"success": False, "error": result["error"], "message": result["message"]}), 400
    
    # Success case
    if "success" in result and result["success"]:
        # Remove password from response
        user_data = result["user"].copy()
        if "password" in user_data:
            del user_data["password"]
            
        return jsonify({"success": True, "user": user_data})
    
    # Fallback error
    return jsonify({"success": False, "message": "Authentication failed"}), 401