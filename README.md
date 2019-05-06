# Cornellender
Final project for CS 1998. A simple calendar app for events.

Description:
  Cornellendar is an iOS App that displays events happening on Cornell Campus. 
  
Backend:
Requirements:
1. Used SQLAlchemy to create a database which allows data to persist.
2. Created several GET requests as well as POST requests to interact with the database created using SQLAlchemy. Also a DELETE request was implemented.
3. Deployed the app to Google Cloud. This can be accessed through the following links.
main page: http://34.74.152.70
all events:http://34.74.152.70/events/
4. Included picture links in my database to allow the IOS code be able to access the pictures for the specific events using information from my database. 

  
iOS:
Requirements:
1. For all layouts in view controllers, we have implemented AutoLayout using NSLayoutConstraints
2. In the root navigation controller, a Collection View Controller and a Table View Controller. 
   The Collection View Controller displays the filters that categorized the events. Pressing on one of the filters will change    the event displayed in the Table View Controller. Only events under the categories selected will be displayed. 
3. When the user click on the cell, a Modal View Controller will be pushed up to show detailed information about the event.
4. Intergrated with backend API.

Special features:
1. A search bar is implemented, which allows users to directly search any event that they are interested in based on the          keyword. Users can also use the search bar combined with a category filter.
2. Within the event detailed view, a map is presented allowing users to have a better understanding of where the event will be    held.
  
