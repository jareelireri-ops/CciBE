from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

# Mock Staff Directory
staffDirectory = [
  { 
    "name": "Jareel Ireri", 
    "username": "jareel", 
    "password": "Jahisreal", 
    "role": "MEDIA",
    "permissions": ['live_buttons', 'sermons', 'announcements', 'events']
  },
  { 
    "name": "David Kagwa", 
    "username": "david", 
    "password": "kipipiri", 
    "role": "SUPER", 
    "permissions": ['all']
  }
]

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    found_user = next((u for u in staffDirectory if u['username'] == username and u['password'] == password), None)
    
    if found_user:
        return jsonify({"success": True, "user": found_user})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
