'''
->Purpose: 
    The following program allows scraping information about from specific websites


->Goals:
     a) Discover new startups in bulk 
     b) Dig into a specific startup and find out everything new there is to know about it

->ToDo:
    a) Build a function that takes a url as parameter, and captures a screenshot of a website and saves it in the current director with the filename being "[website name]-[date].jpg"
    b) Build a function that takes a url as parameter, and searches crunchbase.com for that website and finds out and prints everything we can know from crunchbase about that company

->Imports:

'''

import time
from datetime import date
import pdfkit





def html_to_pdf(url):
    '''
       ->Purpose: The following function converts html to pdf
       ->Output: pdf file containing screenshot of website front page
    '''
    path_wkhtmltopdf = r"C:\Users\mhsha\anaconda3\Lib\site-packages\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url(url, "tesla.pdf", configuration=config)
    

if __name__ == "__main__":
    name = input('Enter name of website, no need for https:// or www. or .com \n-> eg: pinterest: ')
    url = 'https://www.' + name + '.com/'
    html_to_pdf(url)
    
