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
  
  os: used to get path for saving tokens and credentials
         
 
'''
import yaml
import gcsa
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
            
            #Print to show user that it is authenticating and which email address they should use to sign in
            print("{}{} {}".format(key2,':', value2))
            
            #Perform authentication using the value of name_calendar_ids_dict, the value is the Calendar ID
            calendar = GoogleCalendar(calendar=value1, credentials_path=path_credentials, token_path=path_tokens, save_token=True)
            
            #Create an entry in name_calendar_dict, the key is the name and value is authorized calendar
            category_obj.name_calendar_dict[key1] = calendar
            file_id += 1
    
               
    return


def get_timeline():
    '''
    The following function prompts the user for the timeframe they want to extract events, if no timeframe then use default of -30/+15 from current day 
    '''
    invalid_response = True
    while invalid_response:
        
        timeframe = input("Enter 'timeframe' to specify start and end dates or enter 'default' to use -30/+15 days from current day: ")
        if timeframe == 'timeframe' or timeframe == 'default':
            invalid_response = False
        else:
            invalid_response = True
        
    if timeframe == 'timeframe':
        invalid_date = True
        while invalid_date is True:
            start_date = input("Enter the start date mm/dd/yyyy: ")
            end_date = input("Enter the end date mm/dd/yyyy: ")
            try:
                start_date = datetime.strptime(start_date, "%m/%d/%Y")
                end_date = datetime.strptime(end_date, "%m/%d/%Y")
                invalid_date = False
            except ValueError:
                print("\nError: date does not match format: mm/dd/yyyy")
                invalid_date = True
        
    else:
        start_date = (datetime.today() - timedelta(days=30)).date()
        end_date = (datetime.today() + timedelta(days=15)).date()
        
    return start_date, end_date
    
    
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
    events_between_dates = calendar.get_events(time_min=start,time_max=end,order_by='startTime',single_events=singleEvents)
    
    return events_between_dates

def object_introspection_using_pandas(categories_objs, start, end):
    '''
    The following function creates eight columns:  Category,Calendar,Event Description, Start Time, End Time, Day, Month, Year
    We will iterate over the list of Category objects, access their Google Calendar object and call get_events() on it. We will 
    then iterate over the events, extracting the description, start and end time as well the day/month/year
    '''
    
    #Create an empty dataframe with eight columns: Category,Calendar,Event Description, Start Time, End Time, Day, Month, Year
    categorized_df = pd.DataFrame(columns=['Category','Calendar','Event Description', 'Shared', 'Un-Shared', 'Start Date', 'End Date', 'Start Time', 'End Time'])
    
   
    #Iterate over Category objects, calling the get_events mehtod on their Google Calendar, extracting the category name, calendar name and add to DataFrame
    for category_obj in categories_obj.list_of_Category_objs:
        for name,calendar in category_obj.name_calendar_dict.items():
            
            #Call get_events to get events from specified Google Calendar
            events = get_events(calendar,start, end, True)
            for event in events:
                
                unshared = False
                shared = False
                category = category_obj.name
                calendar_name = name
                desp = getattr(event, "summary")
                
                #Extract start and end date, these are both datetime objects
                start_of_event = getattr(event, "start")
                end_of_event = getattr(event, "end")
                
                #Convert the datetime objects into strings using strftime for adding to dataframe
                start_date = start_of_event.strftime("%m/%d/%Y")
                start_time = start_of_event.strftime("%H:%M:%S")
                end_date = end_of_event.strftime("%m/%d/%Y")
                end_time = end_of_event.strftime("%H:%M:%S")
                
                #For reminders such as Birthdays, since they do not have duration
                if start_time == "00:00:00" and end_time == "00:00:00":
                    end_date = start_date
                
                #Get the attendees of the respective event
                attendees_of_event = getattr(event, "attendees")
                
                 #If no attendees present it is a presonal event
                if len(attendees_of_event) == 0:
                     unshared = True
                else:
                     shared = True
                #Create a new entry to add to the DataFrame
                new_event_series = pd.Series(data = [category, calendar_name, desp, shared, unshared, start_date, end_date, start_time, end_time ], index=categorized_df.columns)
                
                #Add to the Dataframe
                categorized_df = categorized_df.append(new_event_series, ignore_index = True)
                
    return categorized_df    
   
def analysis(categorized_df, start, end):
    ''' 
    The following function analyzes the dataframe created, informing the user the percentage of time they spent in the specified categories over
    the timeframe mentioned
    '''
    df = categorized_df
    start = start.strftime("%m/%d")
    end = end.strftime("%m/%d")
    
    df['Start'] = pd.to_datetime(categorized_df['Start Date']+' '+categorized_df['Start Time'])
    df['End'] =   pd.to_datetime(categorized_df['End Date']+' '+categorized_df['End Time'])
    df['Duration'] = ((df['End'] - df['Start']).dt.seconds) / 3600
    df['Day']= df['Start'].dt.day_name()
    df['Day'] = pd.Categorical(df['Day'], categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],ordered=True)
    
    
    
    fig, axes = plt.subplots(nrows=2, ncols=2,dpi=50)
  
    #Plot % Time Spent per Category between timeframe specified 
    title = '% Time Spent ' +start+ " - " +end
    df.groupby('Category')['Duration'].sum().plot( kind = 'pie', autopct='%1.2f%%', ax=axes[0,0], title = title, figsize=(10,10))
    plt.xlabel(None)
    plt.ylabel(None)
     
    
    #Plot the average time spent per category 
    title = 'Average Time Spent ' +start+ " - " +end
    df.groupby("Category").agg({"Duration" : np.mean}).plot(kind = 'barh', ax=axes[0,1], title=title, figsize=(10,10))
    xlabel = 'Hours'
    ylabel = 'Category'
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
     
    #Average Time spent per Category in a Week
    title = 'Average Hours Spent Per Category in a Week'
    week = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df.groupby(['Day', 'Category'])['Duration'].mean().sort_index().unstack().plot(kind='bar', ax=axes[1,0], title=title, figsize=(10,10))
    xlabel = 'Day'
    ylabel = 'Category'
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    #Plot the % Time Spent per Calendar for every category
    title = 'Time Spent Per Calendar ' +start+ " - " +end
    df.groupby(['Category','Calendar'])['Duration'].sum().unstack().plot(kind='bar', ax=axes[1,1], title = title, figsize=(10,10))
    xlabel = 'Category'
    ylabel = 'Hours'
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.savefig('results.png')
     

    
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
    start_date, end_date = get_timeline()
    categorized_df = object_introspection_using_pandas(categories_obj, start_date, end_date)
    byCategory_df = analysis(categorized_df, start_date, end_date)