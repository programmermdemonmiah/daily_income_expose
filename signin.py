from flask import Blueprint, jsonify, request
import bcrypt
import jwt
from db import get_db_connection

signin_bp = Blueprint('signin_bp', __name__)

@signin_bp.route('/signin', methods=['POST'])
def signin_user():
    try:
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'message': 'Unsupported Media Type. Please use Content-Type: application/json.'}), 415
        

        if not request.data.strip():
            return jsonify({'message': 'phone and password are required'})
        
        data = request.json
        phone = str(data.get('phone')) if data.get('phone') else None
        password = str(data.get('password')).strip() if data.get('password') else None

        if not phone or not password:
            return jsonify({'message': 'phone and password are required'}), 400
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                SELECT user_id, name, phone, password FROM user_info WHERE phone = %s
                ''', (phone,)
            )
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if not user:
                return jsonify({'message': 'Invalid phone number or password'}), 401
            
            
            # Check password
            hashed_password = user[3]
            # print(f'{hashed_password}')
            # print(f'pass : {bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))}')

            if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                # Generate JWT token
                # print('call')
                token_payload = {'name': str(user[1]), 'phone': phone}
                token = jwt.encode(token_payload, 'programmermdemonmiah', algorithm='HS256')
                # print('call')
                return jsonify({'message': 'Logged in successfully', 'token': token}), 200
            else:
                return jsonify({'message': 'Invalid phone number or password'}), 401

    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500
