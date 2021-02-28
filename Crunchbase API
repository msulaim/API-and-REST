'''
Purpose: Consume the Crunchbase API using Python to leverage data related to companies 
belonging to a certain industry. The type of industry and the number of companies 
are entered by the user.
'''
import requests
import json
import string
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

def get_data(typeEntered = "company", user_key = "d059f39b8f5fd5095490a564838fec8a"):
    '''
    Input Values: typeEntered (string) = organiztion type specified by the user , user_key (string) 
    
    The following function uses the get method, along with the query parameters passed,
    (organization_types) into the function to get data from the crunchbase website. The
    results are the Organzation Summary of companies realted to the organiztion type 
    specified by the user. 
    
    Return Value: list containing company dictionaries, where each company has a name as key and description as value
    '''
    #Base URL for basic access, only ODM organizations can be used
    _url = "https://api.crunchbase.com/v3.1/odm-organizations"
    
    #Specifying endpoints by passing query parameters, these include
    #organization_type, sort_order, page and user_key
    query_params = {"organization_types": typeEntered , "sort_order":"created_at DESC","page":"1","user_key":"d059f39b8f5fd5095490a564838fec8a"}
    
    #Get data from Crunchbase
    resp = requests.get(url=_url, params=query_params,)
    
    #Extracting data in JSON format or Desrializing, can use json.loads() alternatively
    #Converted to a Python dictionary
    data = resp.json()
    
    #We are only interested in the items inside the data dictionary, not the metadata
    data = data["data"]["items"]
    
    #Dictionary to contain companies, key will be name and value will be short
    #description
    
    organizations = []
    
    # What data looks like data["data"]["items"][0]["properties"]["short_description"]
    for company in data:
        
        company_dict = {}
        #We are interested in the properties of each company
        name = company["properties"]["name"]
        short_desp = company["properties"]["short_description"]
        
        #Create dictionary for company
        company_dict["name"] = name
        company_dict["short_description"] = short_desp
        #Add dictionary to list of companies 
        organizations.append(company_dict)
    
            
    #Writing data to JSON file for viewing JSON objects
    with open("organizations_data.json", "w") as file_write:
        json.dump(organizations,file_write)
    
    return organizations

def get_categories():
    '''
    The following function gets the JSON object from JSON blob
    
    Return Value = returns the data related to categories, 14 categories
    in total, each has a name and associated keywords
    '''

    #Endpoint is the user _id of JSON object created online
    _url = "https://jsonblob.com/c58c395b-79fd-11eb-8c0b-51da211f4965"
    
    #Get the JSON object
    response = requests.get(_url)

    #Extracts data and converts to python form
    data = response.json()
    
    return data
    
    


def processor(organizations, keyword):
    '''
    Input Value = dictionary containing companies, where each company has a name as key and description as value
    and keyword entered by user
    
    The following function accesses the description of each company and performs tokenization, remove stopwords and stem words.
        
    
    '''
    #Download tokens
    nltk.download('punkt')
    
    #Download stopwords
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    
    #Download wordnet
    nltk.download('wordnet')
    
    #regex to remove punctuations
    p = re.compile(r'[?,!.;:\n]')
    
    #Create Lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    #Create Stemmer
    stemmer = PorterStemmer()
    
    #Create regex of keyword
    keyword = stemmer.stem(keyword)
    match = re.compile(keyword)
    
    #List to contain companies whose description contains the keyword
    result_list = []
    
    #Iterate through companies, accessing their description and performing processing on them
    for company in organizations:
        desp = company["short_description"]
        desp = p.sub('',desp) 
        
        #Tokenize
        desp_tokens = desp.split()
        
        #Remove stopwords
        desp_tokens_clean = [word.lower() for word in desp_tokens if word.lower() not in stop] 
        
        #Lematizing#Stemming
        desp_tokens_clean_lem = [stemmer.stem(word) for word in desp_tokens_clean]
        
        desp_tokens_clean_lem_string = ' '.join(desp_tokens_clean_lem)
       
        #Check if user's key-word is contained in company's description
        result = match.search(desp_tokens_clean_lem_string)
        
        if result is not None:
            result_list.append(company)
    print(result_list)
   # print(desp_tokens)
   # print("Clean Tokens")
   # print(desp_tokens_clean)
   # print("Lemmatized Tokens")
   # print(desp_tokens_clean_lem)
    
    
    return
if __name__ == "__main__":
    
    
    #user_key = input("Enter the 32 digit user key: ")
    
    #print("\nChoose from the following types of organizations: {} , {} , {}, {}".format("company", "investor", "school", "group"))
    #typeofCompany = input("Enter the type of organization you are interested in: ")   
    
    organizations = get_data()
    processor(organizations, "finance")
