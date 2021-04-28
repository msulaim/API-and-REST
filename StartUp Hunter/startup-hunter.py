'''
->Purpose: 
    The following program allows scraping information about from specific websites


->Goals:
     a) Discover new startups in bulk 
     b) Dig into a specific startup and find out everything new there is to know about it

->ToDo:
    a) Build a function that takes a url as parameter, and saves pdf of a website and saves it in the current director with the filename being "[website name]-[date].pdf"
    b) Build a function that takes a url as parameter, and searches crunchbase.com for that website and finds out and prints everything we can know from crunchbase about that company

->Done:
    a) Only for Windows
    
->Imports:

'''

import time
from datetime import date 
import pdfkit
import os
import platform
import wkhtmltopdf

def html_to_pdf(url, name):
    '''
       ->Purpose: The following function converts html to pdf
       ->Input: url ~ string
                name ~ string
       ->Output: pdf file containing screenshot of website front page
    '''
    #Today's date
    today = date.today()
    today = today.strftime("%m-%d-%y")
    
    #Name of Outfile
    outfile = '['+name+']'+'['+today+']'+'.pdf'
    
    #Install the binary file (.exe, .pkg)
    #For Windows it will create a folder called 'wkhtmltopdf' in C:\Program Files, copy the folder to the directroy in which code is present
    
    # ~ Need to determine installation for Mac
    
    #For Windows, path is to an .exe
    if platform.system() == 'Windows':
        path = os.path.join(os.getcwd(),'wkhtmltopdf','bin','wkhtmltopdf.exe')
    
    #For Mac, path is to a .pkg
    elif platform.system() == 'Darwin':
        path = os.path.join(os.getcwd(),'wkhtmltopdf','bin','wkhtmltopdf.pkg')
    
    config = pdfkit.configuration(wkhtmltopdf=path)
    
    try:
        pdfkit.from_url(url, outfile, configuration=config)   
    except pdfkit.HostNotFoundError:
        print('Invalid Website Name')


if __name__ == "__main__":
    name = input('Enter name of website, no need for https:// or www. or .com \n-> eg: pinterest: ')
    url = 'https://www.' + name + '.com/'
    html_to_pdf(url, name)
    