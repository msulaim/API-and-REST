#Consume the Calendar API using HTTP methods such as get, post, put and delete
#Import the requests library
import requests

#Constrcuts the full URL to make the API call relative the path
def _url(path):
    return 'http://localhost:5000/calendar/api/v1.0/events'+path

#Gets all the events using the get method
def get_events():

    return requests.get(_url('/all'))

#Adds a new event using the post method
def add_event():
    
   new_event = {"id": 3 , "title": "Dinner", "user": "Hamdan", "audience": "Ahsan", "date": "03-14", "location": "4th Street"}
   return requests.post(_url(''), json=new_event)   

#Updates a field in the event
def update_event(date):
    
    return requests.put(_url(date), json={"new_date":"02-26"})

#Deletes an event using the delete method
def delete_event(title_ofevent_todelete):
    
    return requests.delete(_url(title_ofevent_todelete)) 
'''
new_event = {"id": 3 , "title": "Dinner", "user": "Hamdan", "audience": "Ahsan", "date": "03-14", "location": "4th Street"}
resp = requests.post('http://localhost:5000/calendar/api/v1.0/events', json=new_event)
print('Created new event!\n{} {} {} {} {} {}'.format(resp.json()[-1]['id'], resp.json()[-1]['title'], resp.json()[-1]['user'], resp.json()[-1]['audience'], resp.json()[-1]['date'], resp.json()[-1]['location']))
resp_post = requests.put('http://localhost:5000/calendar/api/v1.0/events/02-25', json={"new_date":"02-26"})
get_events()
resp_delete = requests.delete('http://localhost:5000/calendar/api/v1.0/events/Dinner')
get_events()
'''
#Prints the events by using the get method
def print_events():
    resp = get_events()
    for event in resp.json():
            print('{} {} {} {} {}'.format(event['id'], event['title'], event['user'], event['audience'], event['date']))
    print('\n')

print('Calendar 2021')
print_events()
resp = add_event()
print('Created new event!\n{} {} {} {} {} {}'.format(resp.json()[-1]['id'], resp.json()[-1]['title'], resp.json()[-1]['user'], resp.json()[-1]['audience'], resp.json()[-1]['date'], resp.json()[-1]['location']))
print('\nUpdated date 02-25!')
resp = update_event('/02-25')
print_events()
print('Deleted Dinner event!')
resp = delete_event('/Dinner')
print_events()
