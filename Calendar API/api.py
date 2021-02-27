#Designing a web service or API that adheres to REST guidleines. We want to write a calendar application and we want to design a web service for it. The clients of our web service will be asking the serivce to add, remove, and modify events. 
#Importing the flask library
import flask
from flask import request, jsonify, abort, make_response

#Creating a Flask application object
app = flask.Flask(__name__)
#Starts the debugger
app.config["DEBUG"] = True

#Create test data in the form of a list of dictionaries containing key and value pairs
calendar = [{'id':0 , 'title': 'Meeting' , 'user': 'Hamdan', 'audience': 'Danish', 'date':'02-25'},{'id':1 , 'title':'Birthday', 'user': 'Hamdan', 'audience': 'Ali', 'date':'05-23'} , {'id':2, 'title': 'Anniversary', 'user': 'Hamdan', 'audience': 'Shoaib', 'date':'02-15'}]

#Maps URL to functions, this process is called routing. Flask maps HTTP requests to Python fuction, in this case we have mapped one URL path '/' to one function home. Since no additional path has been mapped to the function, Flask runs the code in the function and displays the result in the browser
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Calendar 2021</h1><p>A prototype API for viewing events listed on your calendar</p>'''

#A route to return all of the available events in our calendar, we decide on the root URL ourselves. Our root URL includes the name of the application and the version of the API.Since this is a simple applicationour only resource will be the events in our calendar. Resources are represented by URLs, the client sends requests to these URLs using the methods defined by the HTTP prtocol The REST API leverages HTTP methods, in this case it is using the GET method to fetch data or obtain information about the resource. The URL used to get data should be like this-> http://[hostname]/calendar/api/v1.0/events/all . Data is return in JSON format. JSON objects are like Python's dictionaries.

@app.route('/calendar/api/v1.0/events/all', methods=['GET'])
def get_events():
   
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(calendar), 200, headers)

#In the following function we get the id of the event in the URL, Flask translates it into event_id argument that we pass in the function. We use this argument to search our events arrays, if the id does not exist then we return the 404 error code which according to HTTP sepcification means "Resource Not Found"
@app.route('/calendar/api/v1.0/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    
    results = [event for event in calendar if event['id'] == event_id]
    
    if len(results) == 0:
        abort(404)
    
    return jsonify({'event': results[0]})

#We can do error handling using make_response, this requires three arguments a JSON object or message, a code like 404 or 201 and headers are optional
@app.errorhandler(404)
def not_found(error):
    
	return make_response(jsonify({'Error': 'Not Found'}), 404)

#We can use the POST method to insert a new event into our calendar
@app.route('/calendar/api/v1.0/events', methods=['POST'])
def create_task():
    
    new_event = {'id' : request.json['id'], 'title': request.json['title'], 'user': request.json['user'], 'audience' : request.json['audience'] , 'date' : request.json['date'], 'location' : request.json['location']}
    calendar.append(new_event)
    return jsonify(calendar)

#We can use the PUT method to update data
@app.route('/calendar/api/v1.0/events/<string:date_tochange>', methods=['PUT'])
def update_event(date_tochange):
    
    new_date_event = [event for event in calendar if event['date'] == date_tochange]
    new_date_event[0]['date'] = request.json['new_date']

    return jsonify(new_date_event)
#We can the DELETE method to delete event
@app.route('/calendar/api/v1.0/events/<string:title_ofevent_toremove>', methods=['DELETE'])
def delete_event(title_ofevent_toremove):

    event_to_remove = [event for event in calendar if event['title'] == title_ofevent_toremove]
    calendar.remove(event_to_remove[0])
    
    return jsonify(calendar)
app.run()
