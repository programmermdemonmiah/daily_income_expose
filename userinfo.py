from flask import Blueprint, jsonify, request
from collections import OrderedDict
from db import get_db_connection
import mysql.connector

# Blueprint definition
user_info_bp = Blueprint('user_info_bp', __name__)

# Route definition
@user_info_bp.route('/userinfo', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user_info WHERE user_id = %s', (user_id,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            # Convert data to list of dictionaries for better JSON serialization
            user_info_list = []
            for row in data:
                user_info_list.append({
                    'user_id': row[0],
                    'name': row[1],
                    'age': row[2]
                })

            # Return JSON response using jsonify
            return jsonify(user_info_list)

        except mysql.connector.Error as e:
            print(f"Error executing SQL query: {e}")
            return jsonify({'error': 'Database error'})

    else:
        return jsonify({'error': 'Database connection error'})
