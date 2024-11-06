# Event class 

# Using database connection
from db import get_connection

from flask import jsonify

class Event:
    def __init__(self, EventID, Name, Tags, Price, Description, Photo, Audience, DateTime, Status, Organizer):
        self.__EventID = EventID
        self.Name = Name
        self.Tags = Tags
        self.Price = Price
        self.Description = Description
        self.Photo = Photo
        self.Audience = Audience 
        self.DateTime = DateTime 
        self.Status = Status 
        self.Organizer = Organizer 

    # Not implemented in sprint 1
    def addDiscussion(self):
        pass

    # Returns event details 
    def loadEvent(self):
        # Gather user info into a dictionary
        event_info = {
            "Name": self.Name,
            "Tags": self.Tags,
            "Price": self.Price,
            "Description": self.Description,
            "Photo": self.Photo, 
            "Audience": self.Audience,
            "DateTime": self.DateTime, 
            "Status" : self.Status, 
            "Organizer": self.Organizer
            # Add other profile-related fields here as needed
        }

        return jsonify(event_info)
    
    def listEvents(self):
        sql_insert_query = """SELECT FROM appEvents * """
        data_to_insert = (userName)

        try:
            self.cursor.execute(sql_insert_query, data_to_insert)
            self.connection.commit()
            print("Record inserted successfully")
        except Error as e:
            print("Failed to insert record into MySQL table:", e)
    


    
   
class ImageType:
    def __init__(self, png, jpg, bmp, svg):
        self.png = png
        self.jpg = jpg
        self.bmp = bmp
        self.svg = svg
