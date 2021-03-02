'''
Google Calendar Simple API or gcs is a library that simplifies event management
in a Google calendar, it is a Python oreinted adapter for the official Google Calendar API
'''
import gcsa
import json
from gcsa.event import Event
from gcsa.recurrence import *
from beautiful_date import Mar
from gcsa.google_calendar import GoogleCalendar, SendUpdatesMode
from gcsa.attendee import Attendee
from gcsa.reminders import EmailReminder, PopupReminder

def get_events():
    start =  (1 / Mar / 2021)[12:00]
    date = (31 / Mar / 2021)[12:00]
    single_events = True
    return calendar.get_events(start,end,order_by='updated',single_events=True)
#Authentication for accessing Google Calendar

calendar = GoogleCalendar('mhamdansulaiman@gmail.com',save_token=False)

# # #Create Start and End Date Object
start = (1 / Mar / 2021)[12:00]
end= (31 / Mar / 2021)[12:00]

#Get all events during this time frame 01/03/2021 to 31/03/2021 and write to outfile
#events = calendar.get_events(start,end,order_by='updated',single_events=True)
events = get_events()
with open('get_events.json', 'w') as outfile:
    for event in events:
        json.dump(event,outfile)


    
#Create a new event in calendar using Event object, demonstrate recurrence, the follwoing event happens every 2 weeks, on Tuesday and Thrusday
attendee = Attendee('dtmunir@gmail.com', display_name='Friend')
event = Event(
    'Test Meeting', 
    start=(2 / Mar / 2021)[9:00],
    attendees=attendee,
    recurrence= Recurrence.rule(freq=WEEKLY,
                interval=1,
                count=8,
                by_week_day=[TU, TH]),
    reminders=EmailReminder(minutes_before_start=30)
    )


# calendar.add_event(event, send_updates='all' )

#Get a single event from its title
test_event = calendar.get_events(query="Test Meeting")  
with open('get_test_event.txt', 'w') as outfile:
    for event in test_event:
        outfile.write(str(event))
        


# # #Remove Test Meetings from Calendar
# test_event = calendar.get_events(query="Test Meeting")
# for event in test_event:
#     calendar.delete_event(event, send_updates='all')



