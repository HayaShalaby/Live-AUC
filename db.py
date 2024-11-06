# App database connection 

import mysql.connector
from mysql.connector import Error

# Database connection details
db_config = {
    'host': 'bkuitdpmiddscdp4bt05-mysql.services.clever-cloud.com',
    'database': 'bkuitdpmiddscdp4bt05',
    'user': 'uauhuir1bdzbqxy1',
    'password': 'm4vFPm9LNLuAf0ZpBHpr',
    'port': 3306
}

def get_connection():
    """Establish a database connection and return the connection object."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
