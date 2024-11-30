# User class 

# testfile = "C:\Users\Haya\Desktop\Live@AUC\Live-AUC\test.txt"

# Using database connection
from db import get_connection

from flask import Flask, jsonify
from flask_cors import CORS

# Import dbMgr globally
from dbMgr import dbMgr


app = Flask(__name__)
CORS(app)  # Allows React Native frontend to access the backend

class Student:
    def __init__(self, Email):
        self.Email = Email  # Store the email (used to fetch user data from the database)
        self.connection = get_connection()  # Establish a connection to the database 

        # Check if the connection is established
        if self.connection:
            self.cursor = self.connection.cursor()
            self.db_manager = dbMgr(self.connection)

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
    
    # # Gets username from the addUsername function and inserts it into user table in app database 
    # def insertUsername(self, userName):
    #     sql_insert_query = """INSERT INTO users (userName) VALUES (%s, %s)"""
    #     data_to_insert = (userName)

    #     try:
    #         self.cursor.execute(sql_insert_query, data_to_insert)
    #         self.connection.commit()
    #         print("Record inserted successfully")
    #     except Error as e:
    #         print("Failed to insert record into MySQL table:", e)


    # def updateUsername(self, userName, email):
    #     """Update a specific column value in the database."""
    #     sql_update_query = """UPDATE users SET userName = %s WHERE email = %s"""
    #     data_to_update = (userName, email)

    #     try:
    #         self.cursor.execute(sql_update_query, data_to_update)
    #         self.connection.commit()
    #         print("Record updated successfully")
    #     except Error as e:
    #         print("Error while updating record:", e)


    # def updatePFP(self, pfp, email):
    #     """Update a specific column value in the database."""
    #     sql_update_query = """UPDATE users SET column_name = %s WHERE id = %s"""
    #     data_to_update = (pfp, email)

    #     try:
    #         self.cursor.execute(sql_update_query, data_to_update)
    #         self.connection.commit()
    #         print("Record updated successfully")
    #     except Error as e:
    #         print("Error while updating record:", e)


    # # Parses username from user email returned from authentication service 
    # def addUsername(self, email):
    #     # Setting email and username for user 
    #     Email = email
    #     Name = email.split('@')[0] 

    #     # Writing email and username to user table in app database 
    #     self.insertUsername(Name)


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
            print("Step 1: Fetching user interests...")
            if not self.cursor:
                print("Database connection not established.")
                return []

            # Get event IDs user has attended
            event_ids_query = """
            SELECT event_id 
            FROM bkuitdpmiddscdp4bt05.Event_attendees 
            WHERE userEmail = %s
            """
            self.cursor.execute(event_ids_query, (self.Email,))
            event_ids = self.cursor.fetchall()

            print(f"User attended event IDs: {event_ids}")
            event_ids = [row[0] for row in event_ids]

            # Fetch tags based on attended events
            tags = []
            if event_ids:
                placeholders = ", ".join(["%s"] * len(event_ids))
                tags_query = f"""
                SELECT tag 
                FROM bkuitdpmiddscdp4bt05.Event_categories 
                WHERE event_id IN ({placeholders})
                """
                self.cursor.execute(tags_query, tuple(event_ids))
                event_tags = self.cursor.fetchall()

                print(f"Event tags found: {event_tags}")
                tags.extend([row[0] for row in event_tags])

            # Fetch direct user interests
            interests_query = """
            SELECT interest 
            FROM bkuitdpmiddscdp4bt05.Interest 
            WHERE userEmail = %s
            """
            self.cursor.execute(interests_query, (self.Email,))
            user_interests = self.cursor.fetchall()

            print(f"User interests found: {user_interests}")
            tags.extend([row[0] for row in user_interests])

            return list(set(tags))  # Remove duplicates
        except Exception as e:
            print(f"Error fetching interests for user {self.Email}: {e}")
            return []
        # finally:
        #     if self.cursor:
        #         self.cursor.close()
        #     if self.connection:
        #         self.connection.close()

    def search_events_by_tags(self, tags):
        try:
            print("Step 2: Searching for events matching user interests...")
            if not self.cursor:
                print("Database connection not established.")
                return []

            if tags:
                placeholders = ", ".join(["%s"] * len(tags))
                search_query = f"""
                SELECT event_id, eventName, Price, displayPic, eventDesc 
                FROM bkuitdpmiddscdp4bt05.appEvents
                WHERE event_id IN (
                    SELECT event_id 
                    FROM bkuitdpmiddscdp4bt05.Event_categories 
                    WHERE tag IN ({placeholders})
                )
                """
                self.cursor.execute(search_query, tuple(tags))
                event_data = self.cursor.fetchall()

                print(f"Matching events found: {event_data}")
                return [{
                    "event_id": event[0],
                    "event_name": event[1],
                    "event_price": event[2],
                    "displayPic": event[3],
                    "eventDesc": event[4],
                } for event in event_data]
            else:
                print("No tags found for the user.")
                return []
        except Exception as e:
            print(f"Error searching events by tags for user {self.Email}: {e}")
            return []
        # finally:
        #     if self.cursor:
        #         self.cursor.close()
        #     if self.connection:
        #         self.connection.close()

    def filterEvents(self, recommended_events):
        try:
            print("Step 3: Filtering out attended events...")
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

            print(f"Attended event IDs: {attended_event_ids}")
            # Flatten the result into a list of event IDs
            attended_event_ids = [row[0] for row in attended_event_ids]  # Extract event_ids from tuples

            print(f"Attended event IDs after flattening: {attended_event_ids}")

            # Step 2: Filter recommended events by excluding attended ones
            filtered_events = [
                event for event in recommended_events if event["event_id"] not in attended_event_ids
            ]

            print(f"Filtered events: {filtered_events}")
            return filtered_events
        except Exception as e:
            print(f"Error filtering events for user {self.Email}: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()


    def get_recommended_events(self):
        try:
            # Step 1: Get the user's interests (tags of events they've attended and direct interests)
            tags = self.get_user_interests()

            # Step 2: Search for events that match the tags from the user's interests
            matching_events = self.search_events_by_tags(tags)

            print("Step 2: Searching for events matching user interests...")
            print(f"Matching events found: {matching_events}")

            # Step 3: Filter out events the user has already attended
            filtered_events = self.filterEvents(matching_events)

            print(f"Filtered events: {filtered_events}")

            return  filtered_events
        
        except Exception as e:
            print(f"Error generating recommended events for user {self.Email}: {e}")
            return []

    def save_interest(self, user_email, interest):
        try:
            # Check if the interest is valid
            if not interest.strip():
                return {"status": "error", "message": "Interest cannot be empty."}

            # Check for duplicates in the database
            check_query = """
                SELECT * FROM Interests WHERE user_email = %s AND interest = %s
            """
            self.cursor.execute(check_query, (user_email, interest.strip()))
            existing_interest = self.cursor.fetchone()

            if existing_interest:
                return {"status": "error", "message": "Interest already exists for this user."}

            # Insert new interest into the database
            insert_query = """
                INSERT INTO Interests (user_email, interest) VALUES (%s, %s)
            """
            self.cursor.execute(insert_query, (user_email, interest.strip()))
            self.connection.commit()

            return {"status": "success", "message": "Interest saved successfully."}
        except Exception as e:
            print(f"Error saving interest: {e}")
            return {"status": "error", "message": "Failed to save interest."}
        finally:
            self.cursor.close()
            self.connection.close()

    # Method to close the database connection when done
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("MySQL connection is closed")
