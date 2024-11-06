from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)  # Allows React Native frontend to access the backend

testfile = r"C:\Users\Haya\Desktop\Live@AUC\Live-AUC\test.txt"

# Database connection
connection = get_connection()
if connection:
    cursor = connection.cursor()

# API route to add a username
@app.route('/api/user/<string:userEmail>', methods=['GET'])
def addUsername(userEmail):
    # Get the username from email (split on '@' to get the username)
    userName = userEmail.split('@')[0]
    
    # Insert username into the database
    sql_insert_query = """INSERT INTO users (userName) VALUES (%s)"""
    data_to_insert = (userName,)
    
    try:
        cursor.execute(sql_insert_query, data_to_insert)
        connection.commit()
        return jsonify({"message": "Record inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# API route to load profile info
@app.route('/api/user/profile/<string:userEmail>', methods=['GET'])
def loadPInfo(userEmail):
    with open(testfile, 'r') as file:
        for line in file: 
            if userEmail == line.split(",")[0]:
                
                profile_info = {
                    "username": line.split(",")[1],
                    "pfp": line.split(",")[2],
                    "points": line.split(",")[3],
                    "friends": line.split(",")[4],
                    "following": line.split(",")[5]
                    # Add other profile-related fields here as needed
                }

                return jsonify(profile_info)


def close_connection():
    """Close the database connection."""
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("MySQL connection is closed")


if __name__ == '__main__':
    app.run(debug=True)
