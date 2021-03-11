**Purpose**:
- For most working people, it is very easy to lose track of how they are spending their time. 
- Having a tool that quickly analyzes how much and where a user spending their time can be extremely helpful in setting priorities, identifying areas for improvement and making informed decisions. 

**Overview**:
- We want to group events from multiple Google Calendars into categories specified by the user. 
- We also want to provide the user with ways to set their own configurations, such as setting the email addresses whose Google Calendars they want to access, which calendars to use, as well as adding and deleting their own categories.

**Requirements**:
- Python version 3.9.2 or above

**Packages**:
- Use *pip install package name* in case you are missing the packages listed below, you can check if a package exist by using *pip show package_name*
- ***gcsa***: Google Calendar Simple API, we  will be utilizing the *GoogleCalendar* object, *get_method*, *beautiful_date* module
- ***yaml***: Used to read yaml file provided by the user
- ***os***: Used to get path of directory in which code is saved
- ***pandas***: Used to create Dataframe
- ***numpy***: Used for performing operations on DataFrame
- ***matplotlib***: Used for plotting

**Usage**:
- You can either download the .zip file from the API-and REST respository or you can clone the repository using *git clone*
- ***Step 1:***   
  - Go to Calendar API Quickstart using the following link: https://developers.google.com/calendar/quickstart/python#step_1_turn_on_the 
  - Enable the Google Calendar API , download the Client Configuration 
  - Put credentials.json file into a directory called “.credentials”, this directory needs to be in the same place as the code.  
  - The user is also required to create a directory called “.tokens”, this also has to be in the same place as the code. 

- ***Step 2:***
  - To obtain the *Calendar ID* of the Google Calendar you want to categorize on Google Calendars go to the calendar’s *settings and sharing* -> *Integrate calendar*          ->*Calendar ID* 
  - Create a .yaml file which will store your configuration for the program, these configurations will include the email addresses and Calendar IDs for the Google Calendar you want to categorize. Consider the following structure
*Name_of_Category_1:*
   *email_ids:*
      *Name_of_Calendar_1*: *email address_1*
      *Name_of_Calendar_2*: *email_address_2*
   *calendar_ids*:
      *Name_of_Calendar_1*: *Calendar_ID_1*
      *Name_of_Calendar_2*: *Calendar_ID_2*
*Name_of_Category_2:*
   *email_ids:*
      *Name_of_Calendar_3*: *email address_3*
      *Name_of_Calendar_4*: *email_address_4*
   *calendar_ids*:
      *Name_of_Calendar_3*: *Calendar_ID_3*
      *Name_of_Calendar_4*: *Calendar_ID_4*
       
  n
