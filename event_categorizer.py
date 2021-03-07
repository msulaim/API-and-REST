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

    return
if __name__ == "__main__":
    
    config = user_configuration()
