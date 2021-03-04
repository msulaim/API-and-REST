'''
Google Calendar Simple API or gcs is a library that simplifies event management
in a Google calendar, it is a Python oreinted adapter for the official Google Calendar API
'''
import gcsa
import numpy as np
import pandas as pd
from gcsa.event import Event
from gcsa.recurrence import *
from beautiful_date import *
from datetime import datetime, date, time, timedelta
from gcsa.google_calendar import GoogleCalendar, SendUpdatesMode
from gcsa.attendee import Attendee
from gcsa.reminders import EmailReminder, PopupReminder



def object_introspection_for_date_using_pandas(events):
    '''
    The following function creates a dataframe with six columsn: Total, Personal, Shared, Personal hrs, Shared Hrs, Total Hrs
    intially it is empty with no indexes. We iterate over the events in our caledar, using the month/day as
    indexes of our dataframe. If an index is present,it means that day is present and we will update its category of event
    If an event is not present we will create a new series and append it to the dataframe. We will extract information realted to the
    start and end time to determine time spent in each of the categories
    
    '''
    
    #Create an empty dataframe with six columns: Total, Personal, Shared, Personal Hrs, Shared Hrs and Total Hrs
    categorized_df = pd.DataFrame(columns=['Personal','Shared','Total', 'Personal Hrs', 'Shared Hrs', 'Total Hrs'])
    
    #Month Day Year
    mdy = ['month', 'day', 'year']    
    hms = ['hour', 'minute', 'second']
                                           
    
    
    for event in events:
        
        #Categories of events
        personal = False
        shared = False
    
        
        #Extract start date to index into the correct location of the dataframe
        start_of_event = getattr(event, "start")
        start_mdy = [getattr(start_of_event, _mdy) for _mdy in mdy]
        end_of_event = getattr(event, "end")
        end_mdy = [getattr(end_of_event, _mdy) for _mdy in mdy]
        
        #date_str is the month/day string that will used to index into the dataframe
        date_str = str(start_mdy[0])+'/'+str(start_mdy[1])
        
        #Initialize all hours/minutes/seconds to zero, personal events such as Birthdays have no end time thus their time is zero
        start_hour=start_min=start_sec=end_hour=end_min=end_sec = 0
        
        #Get starting and end times
        if hasattr(start_of_event,'hour'):
              start_hms = [getattr(start_of_event, _hms) for _hms in hms]
              end_hms = [getattr(end_of_event, _hms) for _hms in hms]
        
        else:
            start_hms = [0,0,0]
            end_hms = [0,0,0]
        
        #Create a datetime object for start and end date and time
        start_time = datetime(year = start_mdy[2], month = start_mdy[0], day = start_mdy[1] , hour = start_hms[0] , minute = start_hms[1], second = start_hms[2])
        
        end_time = datetime(year = end_mdy[2], month = end_mdy[0], day = end_mdy[1] , hour = end_hms[0] , minute = end_hms[1], second = end_hms[2])
        
        #Determine time spend and convert into hours
        time_spent = end_time - start_time
        time_spent = time_spent.seconds / 3600
        
        #Get the attendees of the respective event
        attendees_of_event = getattr(event, "attendees")
        
        #If no attendees present it is a presonal event
        if len(attendees_of_event) == 0:
            personal = True
        else:
            shared = True
        
        #if the entry does not exist create a new one using the month/day string as the index
        if date_str not in categorized_df.index:
            
            if personal == True:
               
                new_event_series = pd.Series(data=[1,0,0,time_spent,0,0], index=categorized_df.columns, name=date_str)
                
            else:
                
                new_event_series = pd.Series(data=[0,1,0,0,time_spent,0], index=categorized_df.columns, name=date_str)
            
            categorized_df = categorized_df.append(new_event_series)
            
        #if an entry exist access it using month/day string and increment value as well as time
        else:
            if personal == True:
                categorized_df.loc[date_str, 'Personal'] += 1
                categorized_df.loc[date_str, 'Personal Hrs'] += time_spent    
            else:
                categorized_df.loc[date_str, 'Shared'] += 1 
                categorized_df.loc[date_str, 'Shared Hrs'] += time_spent
                
            
        #every event increments the total hours for that day, add hours of both categories to get total hours spent
        categorized_df.loc[date_str, 'Total'] += 1
        categorized_df.loc[date_str, 'Total Hrs'] = categorized_df.loc[date_str, 'Personal Hrs'] + categorized_df.loc[date_str, 'Shared Hrs']  
            
        
    
    print(categorized_df)
    return categorized_df
            


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
    calendar = GoogleCalendar(user_email,save_token=True)
    
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
    events_between_dates = get_events(calendar, (31 / Dec / 2020)[23:00], (31 / Mar / 2021)[23:00], True)
    #write_to_file(events_between_dates)
    # day_month_matrix = create_month_date_matrix()
    # events_matrix, total_events_per_month = object_introspection_for_date_using_numpy(events_between_dates, day_month_matrix)
    # total_number = np.sum(total_events_per_month)
    # print("There were ", total_number, "Events between Jan-March 2021")
    # print("Jan: ",total_events_per_month[0])
    # print("Feb: ",total_events_per_month[1])
    # print("Mar: ",total_events_per_month[2])   
    categorized_df = object_introspection_for_date_using_pandas(events_between_dates)
