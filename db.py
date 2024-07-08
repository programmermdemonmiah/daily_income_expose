#db.py

import mysql.connector



#DB_CONFIG configuration from database
DB_CONFIG = {
    'host': 'localhost',
    'database': 'cmon_db',
    'user': 'root',
    'password': ''
}

# DB_CONFIG = {
#     'host': 'localhost',
#     'database': 'cmon_db',
#     'user': 'root',
#     'password': ''
# }

# Function to establish database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"error connection : {e}")
        return None