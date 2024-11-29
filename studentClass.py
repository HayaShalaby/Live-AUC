# User class 

from mysql.connector import Error

# Using database connection
from db import get_connection

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows React Native frontend to access the backend

class Student:
    def __init__(self, Email):
        self.Email = Email  # Store the email (used to fetch user data from the database)
        self.connection = get_connection()  # Establish a connection to the database

        # Check if the connection is established
        if self.connection:
            self.cursor = self.connection.cursor()

            # SQL query to fetch the user's profile info from the database
            sql_query = """SELECT userName, pfp, points, friends, following, major, phone FROM users WHERE email = %s"""
            self.cursor.execute(sql_query, (self.Email,))  # Execute the query with the provided email
            user_data = self.cursor.fetchone()  # Fetch the result as a single row

            # Print the user_data for debugging purposes
            print("User data fetched:", user_data)
            print(user_data)

            # If user data exists, populate the instance variables
            if user_data:
                self.Name = user_data[0]  # username (first column)
                self.PFP = user_data[1]   # profile picture URL (second column)
                self.Points = user_data[2]  # points (third column)
                self.Friends = user_data[3]  # number of friends (fourth column)
                self.Following = user_data[4]  # number of people the user is following (fifth column)
                self.Major = user_data[5]   # major (sixth column)
                self.Phone = user_data[6]   # phone (seventh column)

            
            else:
                # If the user is not found, handle the case by assigning default values
                self.Name = None
                self.PFP = None
                self.Points = 0
                self.Friends = 0
                self.Following = 0
                self.Major = None
                self.Phone = None
               
        else:
             # If the connection fails, set all attributes to None or default values
            print("Failed to connect to the database")
            self.Name = None
            self.PFP = None
            self.Points = 0
            self.Friends = 0
            self.Following = 0
            self.Major = None
            self.Phone = None
   
    # Method to return the user's profile information as a JSON response
    def loadPInfo(self):
         # Check if user data is available
        if self.Name:
            profile_info = {
                "username": self.Name,
                "pfp": self.PFP,
                "points": self.Points,
                "friends": self.Friends,
                "following": self.Following,
                "major": self.Major,
                "phone": self.Phone
            }
            return jsonify(profile_info)  # Ensure it returns a valid response
        
        # In case user data is missing or not found
        return jsonify({"error": "User not found"}), 404  # Optional error response with status code
    
     # Separate method to load the user's attended events
    
    def load_attended_events(self):
        # Check if the connection exists
        if self.connection:
            # SQL query to fetch event IDs for the given user email
            sql_query = """SELECT event_id FROM Event_attendees WHERE userEmail = %s"""
            self.cursor.execute(sql_query, (self.Email,))  # Execute the query with the provided email
            event_data = self.cursor.fetchall()  # Fetch all the event IDs the user has attended

            # If events are found, return them in a list
            attended_events = [event[0] for event in event_data]  # Extract event IDs from the result
            return attended_events
        else:
            print("Failed to connect to the database for attended events")
            return []

    # authentication function - merna 
    def login(self):
        pass

    def isFirstLog(self, userEmail):
        sql_insert_query = """SELECT * FROM users WHERE email = %s"""
        data_to_insert = (userEmail,)

        self.cursor.execute(sql_insert_query, data_to_insert)

        # Fetch the result of the query
        result = self.cursor.fetchone()

        if result is None: 
            return "User not found: first login"  
        else: 
            return "User found: NOT first login"
        
     # Inserts user's info (first time login)
    
    def insertUserInfo(self, userEmail, fName, lName, major, phoneNo):
        userName = userEmail.split('@')[0] 

        pfp = "https://media.istockphoto.com/id/2181878439/fi/vektori/py%C3%B6re%C3%A4-harmaa-k%C3%A4ytt%C3%A4j%C3%A4kuvake-tummanharmaa-siluetti-vaaleamman-ympyr%C3%A4n-sis%C3%A4ll%C3%A4.jpg?s=1024x1024&w=is&k=20&c=1lDFT0XJYUui3iKcX8MZx6n1EphTrb6-Rvkyffwem-Q="

        sql_insert_query = """INSERT INTO users (email, userName, Fname, Lname, major, friends, pfp, userPassword, phone, points, following) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data_to_insert = (userEmail, userName, fName, lName, major, 0, pfp, "None", phoneNo, 0, 0)

        try:
            self.cursor.execute(sql_insert_query, data_to_insert)
            self.connection.commit()
            return "Record updated successfully", 200  # Return success message with status code
        except Error as e:
            return f"Error while updating record: {e}", 500  # Return error message with status code

    def updateUsername(self, userName, email):
        """Update a specific column value in the database."""
        sql_update_query = """UPDATE users SET userName = %s WHERE email = %s"""
        data_to_update = (userName, email)

        try:
            self.cursor.execute(sql_update_query, data_to_update)
            self.connection.commit()
            return "Record updated successfully", 200  # Return success message with status code
        except Error as e:
            return f"Error while updating record: {e}", 500  # Return error message with status code

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

    def get_user_interests(self):
        try:
            if not self.cursor:
                print("Database connection not established.")
                return []

            # Step 1: Get all event_ids for the user
            event_ids_query = """
            SELECT event_id 
            FROM bkuitdpmiddscdp4bt05.Event_attendees 
            WHERE userEmail = %s
            """
            self.cursor.execute(event_ids_query, (self.Email,))
            event_ids = self.cursor.fetchall()  # Fetch all event_id rows

            # Flatten the result into a list of event_ids
            event_ids = [row[0] for row in event_ids]

            # Initialize an empty list for tags
            tags = []

            # Step 2: Get all tags for the retrieved event_ids
            if event_ids:
                placeholders = ", ".join(["%s"] * len(event_ids))
                tags_query = f"""
                SELECT tag 
                FROM bkuitdpmiddscdp4bt05.Event_categories 
                WHERE event_id IN ({placeholders})
                """
                self.cursor.execute(tags_query, tuple(event_ids))  # Pass event_ids as a tuple
                event_tags = self.cursor.fetchall()  # Fetch all tag rows
                tags.extend([row[0] for row in event_tags])  # Add tags to the list

            # Step 3: Get all interests directly from the Interests table
            interests_query = """
            SELECT interest 
            FROM bkuitdpmiddscdp4bt05.Interest 
            WHERE userEmail = %s
            """
            self.cursor.execute(interests_query, (self.Email,))
            user_interests = self.cursor.fetchall()  # Fetch all interest rows
            tags.extend([row[0] for row in user_interests])  # Add interests to the list

            # Remove duplicates (if any) and return the combined list of tags and interests
            return list(set(tags))
        except Exception as e:
            print(f"Error fetching interests for user {self.Email}: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                
     def filterEvents(self, recommended_events):
        try:
            if not self.cursor:
                print("Database connection not established.")
                return []

            # Step 1: Get all event_ids the user has attended
            attended_events_query = """
            SELECT event_id 
            FROM bkuitdpmiddscdp4bt05.Event_attendees 
            WHERE userEmail = %s
            """
            self.cursor.execute(attended_events_query, (self.Email,))
            attended_event_ids = self.cursor.fetchall()  # Fetch all attended event IDs

            # Flatten the result into a list of attended event IDs
            attended_event_ids = {row[0] for row in attended_event_ids}  # Use a set for faster lookups

            # Step 2: Filter recommended events by excluding attended ones
            filtered_events = [
                event for event in recommended_events if event not in attended_event_ids
            ]

            return filtered_events
        except Exception as e:
            print(f"Error filtering events for user {self.Email}: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                
    # Method to close the database connection when done
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("MySQL connection is closed")
