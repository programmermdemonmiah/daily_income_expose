import json
from typing import OrderedDict
from urllib import response
from flask import Blueprint, jsonify, request
from db import get_db_connection

# Blueprint definition
user_income_bp = Blueprint('user_income_bp', __name__)

# Route definition
@user_income_bp.route('/income', methods=['GET'])

def get_income_info():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT u.user_id, u.name AS user_name, i.amount AS income
                FROM user_info u
                JOIN income i ON u.user_id = i.user_id
                WHERE u.user_id = %s;
            ''', (user_id,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            # Convert data to list of dictionaries for better JSON serialization
            user_income_list = []
            for row in data:
                user_income_list.append({
                    'user_id': row[0],
                    'name': row[1],
                    'income': row[2]
                })

            # Return data as JSON response
            return jsonify(user_income_list)

        except Exception as e:
            return f"Error: {str(e)}"

        finally:
            # Ensure cursor and connection are closed
            if 'cur' in locals():
                cursor.close()

    else:
        return jsonify({'error': 'Database connection error'})

@user_income_bp.route('/income', methods=['POST'])
def user_income_post():
    try:

        # if request.headers['Content-Type'] != 'application/json':
        #  return jsonify({'message': 'Unsupported Media Type. Please use Content-Type: application/json.'}), 415
         
        if not request.data.strip():
            return jsonify({'message': 'User ID and amount are required and fields(user_id, amount, notes)'}), 400
        
        user_id = request.json.get('user_id') 
        amount = request.json.get('amount')
        notes = request.json.get('notes')

        
        if not user_id or not amount:
            return jsonify({'message': 'User ID and amount are required and fields(user_id, amount, notes)'}), 400

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO income (user_id, amount, notes)
                VALUES (%s, %s, %s);
            ''', (user_id, amount, notes,))
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'message': 'Expense added successfully'})

    except Exception as e:
        return jsonify({"message": f"Error: {e}"})

            