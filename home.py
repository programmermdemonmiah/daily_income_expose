from flask import Blueprint, jsonify, request
from db import get_db_connection

user_home_bp = Blueprint("user_home_bp", __name__)

@user_home_bp.route('/home', methods=['GET'])
def get_home_data():
    user_id = request.args.get('userId')
    connection = get_db_connection()  # Call the function to get the connection

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                '''
                SELECT u.user_id, u.name AS name, SUM(i.amount) AS totalIncome, SUM(e.amount) As totalCost
                FROM user_info u
                JOIN income i ON u.user_id = i.user_id
                Join expance e ON u.user_id = e.user_id
                WHERE u.user_id = %s
                GROUP BY u.user_id;
                ''', (user_id,)
            )
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            user_hisab_list = []

            for rowCountData in data:
                user_hisab_list.append({
                    'user_id': rowCountData[0],
                    'name': rowCountData[1],
                    'totalIncome': rowCountData[2],
                    'totalCost': rowCountData[3]
                })
            return jsonify(user_hisab_list)
        except Exception as e:
            return jsonify({"Error": f"{e}"})
        
    else:
        return jsonify({'error': 'Database connection error'})
