from flask import Blueprint, jsonify, request
from db import get_db_connection


user_expance_bp = Blueprint('user_expance_bp', __name__)

@user_expance_bp.route('/expance', methods=['GET'])

def get_expance_info():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT u.user_id, u.name AS user_name, e.amount AS expance
                FROM user_info u
                JOIN expance e ON u.user_id = e.user_id
                WHERE u.user_id = %s;
            ''', (user_id,))
            dataTable = cursor.fetchall()
            cursor.close()
            connection.close()

            user_expanse_list = []
            for rowData in dataTable:
                user_expanse_list.append({
                    "user_id" : rowData[0],
                    "name" : rowData[1],
                    "expance" : rowData[2]

                }) 
            
            return jsonify(user_expanse_list)

        except Exception as e:
            return f"Error: {e}"
    else:
        return jsonify({'error': 'Database connection error'})

@user_expance_bp.route('/expance', methods=['POST'])

def user_expance_post():
    try:
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Unsupported Media Type. Please use Content-Type : application/json.'}), 415
        
        if not request.data.strip():
            return jsonify({'message': 'User ID and amount are required and fields(user_id, amount, notes)'}), 400
        
        user_id = request.json.get('user_id')
        amount = request.json.get('amount')
        notes = request.json.get('notes')

        if not user_id or not amount:
            return jsonify({'error': 'User ID and amount are required and fields(user_id, amount, notes)'}), 400

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO expance (user_id, amount, notes)
                VALUES (%s, %s, %s);
            ''', (user_id, amount, notes,))
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'message': 'income added successfully'})

    except Exception as e:
        return f"Error: {e}"
