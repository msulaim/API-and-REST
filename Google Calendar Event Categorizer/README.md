# Google Calendar Event Categorizer
## Purpose:
- For most working people, it is very easy to lose track of how they are spending their time. 
- Having a tool that quickly analyzes how much and where a user spending their time can be extremely helpful in setting priorities, identifying areas for improvement and making informed decisions. 

## Overview:
- We want to group events from multiple Google Calendars into categories specified by the user. 
- We also want to provide the user with ways to set their own configurations, such as setting the email addresses whose Google Calendars they want to access, which calendars to use, as well as adding and deleting their own categories.

## Requirements:
- Python version 3.9.2 or above

## Packages:
- Use *pip install package name* in case you are missing the packages listed below, you can check if a package exist by using *pip show package_name*
- ***gcsa***: Google Calendar Simple API, we  will be utilizing the *GoogleCalendar* object, *get_method*, *beautiful_date* module
- ***yaml***: Used to read yaml file provided by the user
- ***os***: Used to get path of directory in which code is saved
- ***pandas***: Used to create Dataframe
- ***numpy***: Used for performing operations on DataFrame
- ***matplotlib***: Used for plotting

## Usage:
- You can either download the *.zip* file from the **API-and REST** respository or you can clone the repository using *git clone*
- ### Step 1:   
  - Go to **Calendar API Quickstart** using the following link: https://developers.google.com/calendar/quickstart/python#step_1_turn_on_the 
  - Enable the **Google Calendar API** , download the **Client Configuration** 
  - Put **credentials.json** file into a directory called **“.credentials”**, this directory needs to be in the same place as the code.  
  - The user is also required to create a directory called **“.tokens”**, this also has to be in the same place as the code. 

- ### Step 2:
  - To obtain the **Calendar ID** of the Google Calendar you want to categorize on Google Calendars go to the calendar’s **settings and sharing -> Integrate calendar ->Calendar ID** 
  - Create a **.yaml** file which will store your configuration for the program, these configurations will include the **email addresses** and **Calendar IDs** for the Google Calendar you want to categorize. Consider the structure shown in [Link to sample.yaml](./sample.yaml), alternatively this file can be found in the **Google Calendar Event Categorizer** directory
  - Follow the structure shown exactly, **refrain from adding:** '-' to create members of list, '---' to mark the end of document, '...' to mark the beginning of a document
  - Save the **.yaml** in the same directory as the code

- ### Step 3:
  - Run the code from the command line by using *python categorizer.py* or *python3 categorizer.py*
  - You will be prompted to enter the **name** of the **.yaml** file along with its **extension**
  - If it is your first time running the code, a tab will open in your browser prompting you to **sign in** and allow access to **Quickstart**, ensure that you are **signing into your accounts in the same order as specified in the .yaml file**, additionally the command line will print *Authenticating: Calendar_name : Email Address.*
  - Your sign in information will be stored in a **.pickle** file which will be stored in **".tokens"** directory 

- ### Step 4:
  - You will be prompted to choose between two options, either choose **timeframe** which allows you to specify the **start** and **end** date or **default** which sets the **start** date *30 days ago* and **end** date to *15 days after current date*
 
- ### Step 5:
  - The code could take 2-3 seconds depending on how big a timeframe you have entered, during this time all events in the specified timeframe will be pulled from your Google Calendar, enteries will be created for each one of them in a **Dataframe**, the Dataframe contains columns that specify for the event which **Category** it belongs to for example *Work*, which **Calendar** is it from for example: its from a calendar called *Company-A* , whether it is *Shared* or **Un Shared** for example *the event is a meeting with another user*, the **Start Date, Start Time, End Date** and **End Time**. The **Duration** will be determined by subtracting *End Date+Time* from *Start Date+Time*. The results are then plotted for visualization and saved in **results.png**
  - After the code has stopped running typing in *results.png* in command line will open up the image
  
  ## Results:
  - *results.png* contains a figure containing four subplots: a pie chart *"% Time Spent"* that informs the user what percentage of their time they spent in each category over the timeframe specified, a shorizontal bar chart *"Average TIme Spent Per Category"* which informs the user how much time they spent on average in each category, a stacked bar chart *"Average Time Spent Per Category in a Week"* which informs the user how much on average did they spend in each category every day of the week and lastly a bar chart *"Total Time Spent Per Calendar"* which informs the user how much time they spent in total per calendar
  - []
    

       
  
