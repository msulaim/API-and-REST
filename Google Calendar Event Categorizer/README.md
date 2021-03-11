**Purpose**:
- For most working people, it is very easy to lose track of how they are spending their time. 
- Having a tool that quickly analyzes how much and where a user spending their time can be extremely helpful in setting priorities, identifying areas for improvement and making informed decisions. 

**Overview**:
- We want to group events from multiple Google Calendars into categories specified by the user. 
- We also want to provide the user with ways to set their own configurations, such as setting the email addresses whose Google Calendars they want to access, which calendars to use, as well as adding and deleting their own categories.

**Requirements**:
- Python version 3.9.2 or above

**Packages**:
- Use *pip install package name* in case you are missing the packages listed below, you can check is a package exist by using *pip show package_name*
- ***gcsa***: Google Calendar Simple API, we  will be utilizing the *GoogleCalendar* object, *get_method*, *beautiful_date* module
- ***yaml***: Used to read yaml file provided by the user
- ***os***: Used to get path of directory in which code is saved
- ***pandas***: Used to create Dataframe
- ***numpy***: Used for performing operations on DataFrame
- ***matplotlib***: Used for plotting
