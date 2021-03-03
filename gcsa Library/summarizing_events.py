'''
Google Calendar Simple API or gcs is a library that simplifies event management
in a Google calendar, it is a Python oreinted adapter for the official Google Calendar API
'''
import gcsa
import numpy as np
from gcsa.event import Event
from gcsa.recurrence import *
from beautiful_date import *
from gcsa.google_calendar import GoogleCalendar, SendUpdatesMode
from gcsa.attendee import Attendee
from gcsa.reminders import EmailReminder, PopupReminder

def create_month_date_matrix():
    '''
    The following function creates a [12,31] numpy matrix to keep track of number of events per day
    per month of the format matrix[month-1][day-1][personal, with others, total], personal is 0, with others is 1, total is 2
    
    Return Value: numpy [12,31] matrix
    
    Data Structure: Printing results in the following
        day_month_matrix[12][31] = [0. 0. 0.]
        day_month_matrix[12][31][0] = 0.0
        day_month_matrix[12][31][1] = 0.0
        day_month_matrix[12][30][2] = 0.0
        
        if I set :
            day_month_matrix[12][31][0] = 1
            
        then printing results the following:
            day_month_matrix[12][31] = [1. 0. 0.]
            day_month_matrix[12][31][0] = 1.
            day_month_matrix[12][31][1] = 0.0
            day_month_matrix[12][31][2] = 0.0
                    
    
    '''
    day_month_matrix = np.zeros((12,31,3))
    
    return day_month_matrix


def object_introspection_for_date(events, day_month_matrix):
    '''
    The following function iterates over the events in our caledar, whilst using getattr on the object to get the desired attribute. Since we are
    interested in only the date
    
    Introspection: 
        dir(an_event) -> [ . . . . ,__dict__,  .  . ,’start’, ‘end’, ‘attendees’]
        
        start_of_event = getattr(an_event, “start”)
        type(start_of_event) -> <class 'datetime.datetime'>
        dir(start_of_event) -> [  . . . , ‘day’, ‘month’, ‘year’ , ‘hour’, ‘minute’]
        
         attendees_of_event = getattr(an_event, “attendees”)
        type(attendees_of_event_[0]) -> <class 'gcsa.attendee.Attendee'>
        dir(attendees_of_event_[0]) -> [  . . . , ‘display_name’, ‘email’  . . .]


    '''
    #Create a single dimension array that will store the total number of events per month, 
    #with 12 elements, each element stroes the total numbre of events that month
    total_events_per_month = np.zeros(12, dtype=int)
    
    
    #Type of event
    personal = 0
    with_others = 1
    total = 2
    prev_day = 0
    prev_month = 0 
    for event in events:
        
        #Extract start date to index into the correct location of the day_month_matrix
        start_of_event = getattr(event, "start")
        month = getattr(start_of_event, "month") - 1
        day = getattr(start_of_event, "day") - 1
        
        
        #Get the attendees of the respective event
        attendees_of_event = getattr(event, "attendees")
        
        #If there is only one element in list of attendees, it is personal event, increment value of
        # matrix[month][day][personal]
        if len(attendees_of_event) == 0:
            day_month_matrix[month][day][personal] = day_month_matrix[month][day][personal] + 1
        #If there is more than one attendee, increment value of with_others
        else:
            day_month_matrix[month][day][with_others] = day_month_matrix[month][day][with_others] + 1
            
        #Add events in both presonal and with_others category and store them as the third item in list
        day_month_matrix[month][day][total] = day_month_matrix[month][day][personal] + day_month_matrix[month][day][with_others]

        
         #Get the total number of events per day, using month, index into total_events_per_month and increment
        
        total_events_per_month[month] = total_events_per_month[month] + 1 
        
        if day != prev_day or month != prev_month:
            print("2021-",prev_month+1,"-",prev_day+1,":",day_month_matrix[prev_month][prev_day][total], "Events in total,",day_month_matrix[prev_month][prev_day][personal], "Personal Events,",day_month_matrix[prev_month][prev_day][with_others], "Shared Events" )
        
        prev_day = day
        prev_month = month
    return day_month_matrix, total_events_per_month

def get_events(calendar, start_from, end_at, singleEvents):
    '''
    Input Value: user's calendar, object of type GoogleCalendar
    
    The following function gets all events from the user's google calendar and returns the them
    
    Return Value: Generator object, can be iterated over
    '''
    #Create Start and End Date Object
    start =  start_from
    end = end_at
    
    #Get all events in the time frame specified
    events_between_dates = calendar.get_events(start,end,order_by='startTime',single_events=singleEvents)
    
    return events_between_dates

def authenticate(user_email):
    '''    
    Input Value:user's email, string
    
    The following fucntion performs authentication for accessing Google Calendar
    
    Return Value: returns the user's calendar, object of type GoogleCalendar'
    '''
    calendar = GoogleCalendar(user_email,save_token=False)
    
    return calendar

def create_event(calendar, event_title,start_from, 
                 attendee_email, attendee_name,
                 _freq, _interval, _count, _days, 
                 _min_before_start):
    '''
    Input Value: user's calendar, object of type GoogleCalendar
    
    The following function create a new event in calendar using Event object, demonstrates recurrence, 
    the follwoing event happens every week, on Tuesday and Thrusday and has an attendee
    '''
    attendee = Attendee(attendee_email, display_name=attendee_name)
    event = Event(
        event_title, 
        start=start_from,
        attendees=attendee,
        recurrence= Recurrence.rule(freq=_freq,
                    interval=_interval,
                    count=_count,
                    by_week_day= _days),
        reminders=EmailReminder(minutes_before_start=_min_before_start)
        )


    calendar.add_event(event, send_updates='all' )    
    return

def get_an_event(calendar):
    '''
    Input Value: user's calendar, object of type GoogleCalendar
    
    The following function gets a single event from its title
    
    Return Value: event that was pulled
    '''
    test_event = calendar.get_events(query="Test Meeting")  
    
    return test_event

def delete_event():
    '''
    The following function removes an event from the Calendar based on its title
    '''
    test_event = calendar.get_events(query="Test Meeting")
    for event in test_event:
        calendar.delete_event(event, send_updates='all')


def write_to_file(events_list):
    
    with open('events_list.txt', 'w') as outfile:
        for event in events_list:
            outfile.write(str(event))
            outfile.write("\n")

if __name__ == "__main__":
    
    calendar = authenticate("mhamdansulaiman@gmail.com")
    events_between_dates = get_events(calendar, (1 / Jan / 2021)[12:00], (31 / Mar / 2021)[12:00], True)
    #write_to_file(events_between_dates)
    day_month_matrix = create_month_date_matrix()
    events_matrix, total_events_per_month = object_introspection_for_date(events_between_dates, day_month_matrix)
    total_number = np.sum(total_events_per_month)
    print("There were ", total_number, "Events between Jan-March 2021")
    print("Jan: ",total_events_per_month[0])
    print("Feb: ",total_events_per_month[1])
    print("Mar: ",total_events_per_month[2])   
    
    
    



