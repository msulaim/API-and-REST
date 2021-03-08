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
from gcsa.google_calendar import GoogleCalendar
def user_configuration():
    '''
    Purpose: The following function reads in a .yaml file in the form of a dictionary to determine the
             user's configuration. The .yaml file defines which calendars to use, their Calendar IDs, associated
             email addresses
    
    Output: nested dictionary 
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
            category_obj = Category(key, calendar_ids)
            categories_obj.addTo(category_obj)
    
            
    
    return categories_obj
def authenticate(data):
    '''    
    Input Value:data read from .yaml file, list of nested dictionaries
    
    The following fucntion performs authentication for accessing Google Calendar
    
    Return Value: returns the user's calendar, object of type GoogleCalendar'
    '''
    
    
    return

class Category():
    '''
    A Category object has the following attributes:
        name_calendar_dict : a list of dictionaries, each containing the name of the calendar as the key and
                    and as the value calendars authenticated using GoogleCalendar object from gcsa
        name: the name of the category
    '''
    
    def __init__(self, _nameofCategory, calendar_ids):
        
        #Name of the category for example "Work"
        self.name = _nameofCategory
        
        #Empty list of dictionaries, each containing the name of the calendar as the key and
        #and as the value calendars authenticated using GoogleCalendar object from gcsa
        self.name_calendar_dict = {}
        
        #Contains the nested calendar_ids dictionary, where the keys are the name of the calendar and value is
        #calendar id
        self.calendar_ids_dict = calendar_ids
        
        
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
    
    config = user_configuration()
    #authenticate(config)