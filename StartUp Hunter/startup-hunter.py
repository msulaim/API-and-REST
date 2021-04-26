'''
->Purpose: 
    The following program allows scraping information about from specific websites

'''
'''
->Goals:
     a) Discover new startups in bulk 
     b) Dig into a specific startup and find out everything new there is to know about it
'''
'''
->ToDo:
    a) Build a function that takes a url as parameter, and captures a screenshot of a website and saves it in the current director with the filename being "[website name]-[date].jpg"
    b) Build a function that takes a url as parameter, and searches crunchbase.com for that website and finds out and prints everything we can know from crunchbase about that company
'''
'''
->Imports:

'''
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
import time
import webbrowser
from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
import re

def default_browser():
    '''
    ->Purpose: The following function returns the name for the default browser and installs the required webdriver for it
    
    ->Return: webdriver object for the user's default browser
    '''

    
    path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'

    #Get name of the default browser    
    with OpenKey(HKEY_CURRENT_USER, path) as key:
        default_browser = QueryValueEx(key, 'ProgId')
        default_browser = default_browser[0]
        default_browser = default_browser.lower()
    
    #Dictionary which maps the name of browser to its webdriver function
    name_webdriver_dict = {
                            'chrome': webdriver.Chrome(ChromeDriverManager().install()), 
                            'chromium': webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), 
                            'firefox': webdriver.Firefox(executable_path=GeckoDriverManager().install())
                          }
    #Create regex for matching the name of the default browser and the driver to use 
    for name, web_driver in name_webdriver_dict.items():
        r = re.compile(name)
        if r.match(default_browser):
            driver = web_driver
            break
    
    return driver
    
def screenshot():
    '''
    The following function takes a url as parameter and captures a screenshot of the website, saving the result in the current directory

    '''
    
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install()) 

    driver.get("https://www.youtube.com/")
    time.sleep(1)

    #driver.save_screenshot("screenshot1.jpg")
    driver.quit()
    print("end...")

if __name__ == "__main__":
    default_browser()
    #screenshot()
