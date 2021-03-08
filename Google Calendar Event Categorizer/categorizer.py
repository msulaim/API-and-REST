'''
->Purpose: 
The following program groups events from a user's Google Calendar based on categories specified by
the user in a .yaml file. The .yaml file contains the user's configurations such as the categories,
which calendar to use, email addresses and Calendar IDs
'''

'''
->Imports:
  yaml: to load yaml file provided by the user
  gcsa: Google Calendar Simple API or gcsa is a library that simplifies event management
         in a Google calendar, it is a Python oreinted adapter for the official Google Calendar API.
         We intend to make use of the 
             GoogleCalendar, object: for authentication, 
             get_events(), method: to get all events in a time-frame from the user's specified calendar
  
  beautiful_date: module that can be used for formatting dates 
  
  datetime: module useful for finding duration between two dates
  
  pandas: used to create DataFrames, which is our data strcuture for storing data
         
 
'''
import yaml
import gcsa
import os
import pandas as pd
from beautiful_date import *
from datetime import datetime, date, time, timedelta
from gcsa.google_calendar import GoogleCalendar
def user_configuration():
    '''
    Purpose: The following function reads in a .yaml file in the form of a dictionary to determine the
             user's configuration. The .yaml file defines which calendars to use, their Calendar IDs, associated
             email addresses
    
    Output: Categories object, which contains a list of Category objects 
    '''
    valid_file = False
    
    #Perform file handling, if file cannot be read throw exception and prompt user again
    while not valid_file:
        filename = input('Enter the input file name, including its extension: ')
        try:
            input_file = open(filename, 'r')
            valid_file = True
        except IOError:
            print('There is no file named ', filename)
            invalid_file = False

    #Load the content of the .yaml file, it can contain multiple documents
    data = yaml.load_all(input_file, Loader=yaml.FullLoader)
    
    #Extract the name of the Category, calendar ids and store data in the Category object
    #Add each Category object to the Categories object
    for nested_dicts in data:
        categories = nested_dicts.keys()
        categories_obj = Categories()
        for category in categories:
            key = category
            calendar_ids = nested_dicts[key]["calendar_ids"]
            calendar_email_ids = nested_dicts[key]["email_ids"]
            category_obj = Category(key, calendar_email_ids, calendar_ids)
            categories_obj.addTo(category_obj)
    
            
    
    return categories_obj
def authenticate(categories_obj):
    '''    
    Input Value:data read from .yaml file, list of nested dictionaries
    
    The following fucntion performs authentication for accessing Google Calendar using the calendar ids in a Catgory object
    it adds the name and the created GoogleCalendar to the respective Category object
    '''
    
    #Path to access Google Calendar API crednetials
    path_credentials = os.path.join(os.getcwd(),'.credentials','credentials.json')
    file_id = 1
    
    for category_obj in categories_obj.list_of_Category_objs:
        print("\nAuthenticating")
        for (key1, value1),(key2, value2) in zip(category_obj.name_calendar_ids_dict.items(), category_obj.name_email_id_dict.items()):
            
            #Specify filename and path for the token that will be generated during authentication
            filename = 'token'+str(file_id)+'.pickle'
            path_tokens = os.path.join(os.getcwd(),'.tokens',filename)
            
            #Perform authentication using the value of name_calendar_ids_dict, the value is the Calendar ID
            calendar = GoogleCalendar(calendar=value1, credentials_path=path_credentials, token_path=path_tokens, save_token=True)
            
            #Use the addTo function, to add to the name_calendar_dict which maps the name to the GoogleCalendar Object
            category_obj.addTo(key1,calendar)
            
            #Print to show user that it is authenticating and which email address they should use to sign in
            print("{}{} {}".format(key2,':', value2))
            file_id += 1
    
    return


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

def object_introspection_using_pandas(categories_objs):
    '''
    The following function creates eight columns:  Category,Calendar,Event Description, Start Time, End Time, Day, Month, Year
    We will iterate over the list of Category objects, access their Google Calendar object and call get_events() on it. We will 
    then iterate over the events, extracting the description, start and end time as well the day/month/year
    '''
    
    #Create an empty dataframe with eight columns: Category,Calendar,Event Description, Start Time, End Time, Day, Month, Year
    categorized_df = pd.DataFrame(columns=['Category','Calendar','Event Description', 'Shared', 'Un-Shared', 'Start Time', 'End Time', 'Day', 'Month', 'Year'])
    
    #Month Day Year
    mdy = ['month', 'day', 'year']    
    hms = ['hour', 'minute', 'second']
    
    #Iterate over Category objects, calling the get_events mehtod on their Google Calendar, extracting the category name, calendar name and add to DataFrame
    for category_obj in categories_obj.list_of_Category_objs:
        for name,calendar in category_obj.name_calendar_dict.items():
            
            #Call get_events to get events from specified Google Calendar
            events = get_events(calendar[0],(31 / Dec / 2020)[23:00], (31 / Mar / 2021)[23:00], True)
            for event in events:
                
                unshared = False
                shared = False
                category = category_obj.name
                calendar_name = name
                desp = getattr(event, "summary")
                
                #Extract start and end date
                start_of_event = getattr(event, "start")
                start_mdy = [getattr(start_of_event, _mdy) for _mdy in mdy]
                end_of_event = getattr(event, "end")
                end_mdy = [getattr(end_of_event, _mdy) for _mdy in mdy]
                
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
                        
                #Get the attendees of the respective event
                attendees_of_event = getattr(event, "attendees")
                
                 #If no attendees present it is a presonal event
                if len(attendees_of_event) == 0:
                     unshared = True
                else:
                     shared = True
                #Create a new entry to add to the DataFrame
                new_event_series = pd.Series(data = [category, calendar_name, desp, shared, unshared, start_time, end_time, start_mdy[1], start_mdy[0], start_mdy[2] ], index=categorized_df.columns)
                
                #Add to the Dataframe
                categorized_df = categorized_df.append(new_event_series, ignore_index = True)
                
    return categorized_df
    
   
class Category():
    '''
    A Category object has the following attributes:
        name_calendar_dict : a list of dictionaries, each containing the name of the calendar as the key and
                    and as the value calendars authenticated using GoogleCalendar object from gcsa
        name: the name of the category
    '''
    
    def __init__(self, _nameofCategory, calendar_email_ids, calendar_ids):
        
        #Name of the category for example "Work"
        self.name = _nameofCategory
        
        #Empty list of dictionaries, each containing the name of the calendar as the key and
        #and as the value calendars authenticated using GoogleCalendar object from gcsa
        self.name_calendar_dict = {}
        
        
        #Dictionary where keys are the name of calendar and values are emails
        self.name_email_id_dict = calendar_email_ids
        
        #Contains the nested calendar_ids dictionary, where the keys are the name of the calendar and value is
        #calendar id
        self.name_calendar_ids_dict = calendar_ids
        
        
    def addTo(self, _nameofCalendar, calendar):
        
        '''
        The following function overrides the __add__ method, it sets the key as the name of the calendar
        if there is no calendar in the dictionary create a new list and append to it, if there just append
        '''
        key = _nameofCalendar
        value = calendar
        
        if self.name_calendar_dict.get(key) is None:
            
            self.name_calendar_dict[key] = []
            self.name_calendar_dict[key].append(value)
        
        else:
            self.name_calendar_dict[key].append(value)
            
class Categories():
    
    # Number of Category objects
    count = 0
    '''
    A Categories object stores multiple Category object and has the following attributes:
        list_of_Category_objects: a list containing Category objects
    '''
    def __init__(self):
        self.list_of_Category_objs = []
    
    def addTo(self, Category):
        self.list_of_Category_objs.append(Category)
        Categories.count += 1
        
        
if __name__ == "__main__":
    
    categories_obj = user_configuration()
    authenticate(categories_obj)
    categorized_df = object_introspection_using_pandas(categories_obj)
    