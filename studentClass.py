# User class 

testfile = "C:\Users\Haya\Desktop\Live@AUC\Live-AUC\test.txt"

# Using database connection
from db import get_connection

from flask import jsonify

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your React Native frontend to access the backend

class Student:
    def __init__(self, Email, Name, Major, Phone, Status, Points, Friends):
        self.__Email = Email
        self.Name = Name
        self.Major = Major
        self.Phone = Phone 
        self.Status = Status 
        self.Points = Points 
        self.Friends = Friends
        self.connection = get_connection()
        if self.connection:
            self.cursor = self.connection.cursor()


    def login(self):
        pass
    
    # Gets username from the addUsername function and inserts it into user table in app database 
    def insertUsername(self, userName):
        sql_insert_query = """INSERT INTO users (userName) VALUES (%s, %s)"""
        data_to_insert = (userName)

        try:
            self.cursor.execute(sql_insert_query, data_to_insert)
            self.connection.commit()
            print("Record inserted successfully")
        except Error as e:
            print("Failed to insert record into MySQL table:", e)


    def updateUsername(self, userName, email):
        """Update a specific column value in the database."""
        sql_update_query = """UPDATE users SET userName = %s WHERE email = %s"""
        data_to_update = (userName, email)

        try:
            self.cursor.execute(sql_update_query, data_to_update)
            self.connection.commit()
            print("Record updated successfully")
        except Error as e:
            print("Error while updating record:", e)

    def updatePFP(self, pfp, email):
        """Update a specific column value in the database."""
        sql_update_query = """UPDATE users SET column_name = %s WHERE id = %s"""
        data_to_update = (pfp, email)

        try:
            self.cursor.execute(sql_update_query, data_to_update)
            self.connection.commit()
            print("Record updated successfully")
        except Error as e:
            print("Error while updating record:", e)
    
    # API route that uses UserService
    @app.route('http://192.168.8.103/api/user/<string:userEmail>', methods=['GET'])
    # Parses username from user email returned from authentication service 
    def addUsername(self, email):
        # Setting email and username for user 
        Email = email
        Name = email.split('@')[0] 

        # Writing email and username to user table in app database 
        self.insertUsername(Name)

    
    # Not implemented for sprint 1 
    def saveEvent(self):
        pass
    
    # Not implemented for sprint 1
    def AddFriend(self):
        pass
    
    
    
    # Not implemented for sprint 1 
    def ReportUser(self):
        pass
    
    # Not implemented for sprint 1
    def AddComment(self):
        pass

    # API route that uses UserService
    @app.route('https://636a-156-223-151-38.ngrok-free.app/api/user/<userEmail>', methods=['GET'])
    #Returns username, pfp, points, friends, following 
    def loadProfileInfo (self):
        # Gather user info into a dictionary
        profile_info = {
            "username": self.Name,
            "pfp": self.PFP,
            "points": self.Points,
            "friends": self.Friends
            # Add other profile-related fields here as needed
        }

        return jsonify(profile_info)


    def close_connection(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("MySQL connection is closed")

    # # API route that uses UserService
    # @app.route('http://192.168.8.103/api/user/<string:userEmail>', methods=['GET'])
    # def loadPInfo(self, email):
    #      with open(testfile, 'r') as file:
    #         for line in file: 
    #             if email == line.split(",")[0]:
                
    #                 profile_info = {
    #                     "username": line.split(",")[1],
    #                     "pfp": line.split(",")[2],
    #                     "points": line.split(",")[3],
    #                     "friends": line.split(",")[4],
    #                     "following": line.split(",")[5]
    #                     # Add other profile-related fields here as needed
    #                 }

    #                 return jsonify(profile_info)





