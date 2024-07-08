from flask import Blueprint, jsonify, request
import bcrypt
import jwt 
from db import get_db_connection

# signup_bp = Blueprint('signup_bp', __name__)
signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup_user():
    try:
        if request.headers['Content-Type'] != 'application/json':
         return jsonify({'message': 'Unsupported Media Type. Please use Content-Type: application/json.'}), 415
        
        if not request.data.strip():
            return jsonify({'message': 'name, phone, password are required'}), 400
        
        data = request.json

        name = str(data.get('name')) if data.get('name') else None
        phone = str(data.get('phone')) if data.get('phone') else None
        password = str(data.get('password')) if data.get('password') else None


        if not name or not phone or not password:
            return jsonify({'message': 'name, phone, password are required'}), 400
        

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                INSERT INTO user_info(name, phone, password) VALUES(%s, %s, %s)
                ''', (name, phone, hashed_password)
            )
            connection.commit()
            cursor.close()
            connection.close()

            # Generate JWT token
            token_payload = {'name': name, 'phone': phone}
            token = jwt.encode(token_payload, 'programmermdemonmiah', algorithm='HS256')

            return jsonify({'message': 'Successfully created an account', 'token': token}), 201

    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500
