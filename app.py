from flask import Flask, jsonify, request, redirect, session
from flask_cors import CORS
from db import get_connection
from dbMgr import dbMgr
from eventClass import Event
from studentClass import Student
from datetime import datetime
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

#  test commit 

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enables credentials over CORS
app.secret_key = os.urandom(24)

# Google OAuth configuration
GOOGLE_CLIENT_ID = "995963451857-7jhmon58vpli38p898st5c1oidbf8lpj.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)

# API route to fetch profile info
@app.route('/api/user/profile/<string:userEmail>', methods=['GET'])
def load_user_profile(userEmail):
    # Create an instance of the Student class, passing the email to fetch the user data
    student = Student(userEmail)

    # Get the profile information and return it as JSON
    profile_info = student.loadPInfo()

    # Optionally, close the connection after the operation is complete
    student.close_connection()

    # Return the profile info
    return profile_info

# API route to fetch attended events
@app.route('/api/user/events/<string:userEmail>', methods=['GET'])
def load_user_events(userEmail):
    # Create an instance of the Student class
    student = Student(userEmail)

    # Get the list of attended events for the user
    attended_events = student.load_attended_events()
    
    events = []

    for event in attended_events:
        eventInst = Event(event)
        eventInfo = eventInst.loadEvent()
        events.append(eventInfo)
    return jsonify(events)

# Retrieves all events from db 
def listEvents():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql_query = """
                SELECT event_id, eventName, DatenTime, Price, displayPic, eventDesc
                FROM appEvents
            """
            cursor.execute(sql_query)
            event_data = cursor.fetchall()

            events = [{
                "event_id": event[0],
                "eventName": event[1],
                "DatenTime": event[2].strftime('%Y-%m-%d %H:%M:%S'),
                "Price": float(event[3]),
                "displayPic": event[4],
                "eventDesc": event[5],  # Include eventDesc
            } for event in event_data]

            return events
        except Exception as e:
            print("Error fetching events:", e)
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database")
        return []

# API route to get all events
@app.route('/api/events/homepage', methods=['GET'])
def get_events():
    connection = get_connection()  # Assuming you have a function to establish the database connection
    if connection:
        try:
            cursor = connection.cursor()
            sql_query = """
                SELECT event_id, eventName, DatenTime, Price, displayPic, eventDesc
                FROM appEvents
            """  # Ensure eventDesc is included in the SELECT statement
            cursor.execute(sql_query)
            events = cursor.fetchall()
            results = [{
                "event_id": event[0],
                "event_name": event[1],
                "event_date": event[2].strftime('%Y-%m-%d %H:%M:%S'),
                "event_price": float(event[3]),
                "displayPic": event[4],
                "eventDesc": event[5],  # Include eventDesc
            } for event in events]
            return jsonify(results)
        except Exception as e:
            print(f"Error fetching events: {e}")
            return jsonify({"error": "Failed to fetch events"}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


# Return info for specific event
@app.route('/api/events/specificEvent/<int:event_id>', methods=['GET'])
def load_event_details(event_id):
    # Create an instance of the Event class
    event = Event(event_id)

    # Get the list of attended events for the user
    eventInfo = event.loadEvent()

    # Optionally, close the connection after the operation is complete
    # event.close_connection()

    # Return the attended events as a JSON response
    return jsonify(eventInfo)

# Return whether an event is paid or not (for FE navigation)
@app.route('/api/events/paid/<int:event_id>', methods=['GET'])
def checkPayment(event_id):
    # Create an instance of the Event class
    event = Event(event_id)

    # Get the list of attended events for the user
    paid = event.checkPay()

    # Optionally, close the connection after the operation is complete
    event.close_connection()

    # Return the attended events as a JSON response
    return jsonify(paid)

# Caller function to initiate first-time user in db 
@app.route('/user/init/<string:userEmail>/<string:fName>/<string:lName>/<string:major>/<string:phoneNo>', methods=['PUT'])
def newUser(userEmail, fName, lName, major, phoneNo):
    # Create an instance of the Event class
    student = Student(userEmail)

    message, status_code = student.insertUserInfo(userEmail, fName, lName, major, phoneNo)
    
    # Return the response with the appropriate message and status code
    return jsonify({"message": message}), status_code

# Caller function to return if user is logging in for the first time or not 
@app.route('/user/isFirst/<string:userEmail>', methods=['GET'])
def isFirst(userEmail):
     # Create an instance of the Event class
    student = Student(userEmail)

    message = student.isFirstLog(userEmail)
    
    # Return the response with the appropriate message and status code
    return jsonify({"message": message})

# Caller function to update username for app settings     
@app.route('/api/user/updateUserName/<string:userEmail>/<string:userName>', methods=['PUT'])
def updateUsername(userEmail, userName):
    # Create an instance of the Event class
    student = Student(userEmail)

    message, status_code = student.updateUsername(userName, userEmail)
    
    # Return the response with the appropriate message and status code
    return jsonify({"message": message}), status_code

# Caller function to return event search results 
db_manager = dbMgr(get_connection)
@app.route('/api/search/<string:searchTerm>', methods=['GET'])
def search(searchTerm):
    results = db_manager.search_events(searchTerm)
    return jsonify(results)

##################### Pls write what this function does 
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'OPTIONS':
        return '', 200  # Respond with a 200 status for the OPTIONS request
    data = request.get_json()  # Get the JSON payload from the request
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not event_id or not user_id:
        return jsonify({"error": "event_id and user_id are required"}), 400

    # Check if the event already has an attendees list; if not, initialize it as an empty set
    if event_id not in attendees_db:
        attendees_db[event_id] = set()

    # Check if the user is already registered
    if user_id in attendees_db[event_id]:
        return jsonify({"error": f"User {user_id} is already registered for event {event_id}."}), 400

    # Add the user_id to the event's attendees list
    attendees_db[event_id].add(user_id)

    # Return a confirmation message
    return jsonify({"message": f"User {first_name} {last_name} registered successfully for event {event_id}."})

##################### Pls write what this function does 
@app.route('/login', methods=['GET'])
def login():
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000/callback",
        scope=["openid", "email", "profile"],
    )
    return jsonify({"auth_url": request_uri})

##################### Pls write what this function does 
@app.route('/callback', methods=['GET'])
def callback():
    try:
        code = request.args.get("code")
        print(f"Code received: {code}")

        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        print(f"Google Provider Config: {google_provider_cfg}")

        token_endpoint = google_provider_cfg["token_endpoint"]
        print(f"Token Endpoint: {token_endpoint}")

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url="http://127.0.0.1:5000/callback",
            code=code,
            client_secret=GOOGLE_CLIENT_SECRET,
        )
        print(f"Token Request Prepared: {token_url}, {headers}, {body}")

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        print(f"Token Response: {token_response.status_code}, {token_response.text}")

        client.parse_request_body_response(token_response.text)

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        print(f"User Info Endpoint: {userinfo_endpoint}")

        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        print(f"User Info Response: {userinfo_response.json()}")

        user_info = userinfo_response.json()
        if user_info.get("email_verified"):
            session['user_info'] = {
                "email": user_info["email"],
                "name": user_info["name"],
                "picture": user_info["picture"],
            }
            print(f"User info stored in session: {session['user_info']}")
            return redirect("myapp://logged-in")
        else:
            print("Email not verified")
            return jsonify({"error": "Email not verified"}), 400
    except Exception as e:
        print(f"Callback Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/event/<int:event_id>/check-availability', methods=['GET'])
def check_event_availability(event_id):
    try:
        # Instantiate the Event object with the given event_id
        event = Event(event_id)

        # Call the checkAvail method to check seat availability
        is_available = event.checkAvail()

        # Close the database connection
        event.close_connection()

        # Return the result as JSON
        return jsonify({
            "event_id": event_id,
            "seatsAvailable": is_available
        })
    except Exception as e:
        print(f"Error in /check-availability: {e}")
        return jsonify({"error": "An error occurred while checking availability"}), 500
        
# Endpoint for the React Native app to fetch user data
@app.route('/user-info', methods=['GET'])
def get_user_info():
    if 'user_info' in session:
        return jsonify(session['user_info'])
    return jsonify({"error": "No user is logged in"}), 401

# Recommendation Algorithm that calls all helper functions
@app.route('/api/user/recommendedEvents/<string:userEmail>', methods=['GET'])
def get_recommended_events_route(userEmail):
    try:
        # Create an instance of the Student class with the user's email
        student = Student(userEmail)

        # Call the get_recommended_events method to get recommended events for the user
        recommended_events = student.get_recommended_events()

        if recommended_events:
            return jsonify({"recommendedEvents": recommended_events}), 200
        else:
            return jsonify({"message": "No recommended events found for this user."}), 404
    except Exception as e:
        print(f"Error fetching recommended events for user {userEmail}: {e}")
        return jsonify({"error": "An error occurred while fetching recommended events."}), 500


@app.route('/api/user/interests/<string:userEmail>', methods=['GET'])
def get_user_interests_route(userEmail):
   
    try:
        # Create an instance of the Student class
        student = Student(userEmail)

        # Call the get_user_interests method
        tags = student.get_user_interests()

        # Return the interests as a JSON response
        if tags:
            return jsonify({
                "userEmail": userEmail,
                "interests": tags
            }), 200
        else:
            return jsonify({
                "userEmail": userEmail,
                "interests": [],
                "message": "No interests found for this user."
            }), 404
    except Exception as e:
        print(f"Error fetching interests for user {userEmail}: {e}")
        return jsonify({"error": "An error occurred while fetching interests."}), 500

@app.route('/api/user/interests', methods=['POST'])
def add_interest():
    data = request.get_json()
    user_email = data.get('user_email')
    interests = data.get('interests')

    if not user_email or not interests or len(interests) < 3:
        return jsonify({"status": "error", "message": "user_email and at least 3 interests are required."}), 400

    # Create a Student instance and save the interests
    student = Student(user_email)
    response = student.save_interests(user_email, interests)

    return jsonify(response)
    
# Run app 
if __name__ == '__main__':
    app.run(debug=True)
