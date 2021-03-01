'''
Purpose: Consume the Crunchbase API using Python to leverage data related to companies 
belonging to a certain industry. The type of industry and the number of companies 
are entered by the user.
'''
import requests
import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

def get_data(typeEntered, user_key):
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
    
    #Dictionary to contain companies, key will be name and value will be short
    #description
    organizations = []
    
    for page in range(1,11):
        #Specifying endpoints by passing query parameters, these include
        #organization_type, sort_order, page and user_key
        query_params = {"organization_types": typeEntered , "sort_order":"created_at DESC","page":page,"user_key":user_key}
        
        #Get data from Crunchbase
        resp = requests.get(url=_url, params=query_params,)
        
        #Extracting data in JSON format or Desrializing, can use json.loads() alternatively
        #Converted to a Python dictionary
        data = resp.json()
        
        #We are only interested in the items inside the data dictionary, not the metadata
        data = data["data"]["items"]
        
        
    
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
    outfile = "organizations_data.json"
    with open(outfile, "w") as file_write:
        json.dump(organizations,file_write)
    
    return organizations

def get_keywords(category):
    '''
    Input Value = category specified by user
    
    The following function gets the JSON object from JSON blob
    
    Return Value = returns the data related to categories, 14 categories
    '''
    #Deserialization(reading and decoding JSON objects, string of JSON object)
    with open("categories.json", "r") as read_file:
        data = json.load(read_file)
    
    keys = data["items"]["categories"].keys()
    data = data["items"]["categories"][category]
    
    return data

def get_categories():
    
    '''
    Returns the keys of the dicitonary containing categories and keywords
    '''
    #Deserialization(reading and decoding JSON objects, string of JSON object)
    with open("categories.json", "r") as read_file:
        data = json.load(read_file)
        
    keys = data["items"]["categories"].keys()

    return keys    

def processor(organizations, category, outfile):
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
    
    
    #Get keywords related to category
    keywords = get_keywords(category)
    
    
    #List to contain companies whose description contains the keyword
    results = []
    
    #Iterate through companies, accessing their description and performing processing on them
    for company in organizations:
        desp = company["short_description"]
        desp = p.sub('',desp) 
        
        #Tokenize
        desp_tokens = desp.split()
        keywords_tokens = keywords.split(',')
        
        #Remove stopwords
        desp_tokens_clean = [word.lower() for word in desp_tokens if word.lower() not in stop] 
        keywords_tokens_clean = [word.lower() for word in keywords_tokens if word.lower() not in stop]
        
        #Lematizing#Stemming
        desp_tokens_clean_stem = [stemmer.stem(word) for word in desp_tokens_clean]
        desp_tokens_clean_stem_string = ' '.join(desp_tokens_clean_stem)
        keywords_tokens_clean_stem = [stemmer.stem(word) for word in keywords_tokens_clean]
        
        
        
       #Check if user's key-word is contained in company's description
        for word in keywords_tokens_clean_stem:
            match = re.compile(word)
            found = match.search(desp_tokens_clean_stem_string)
            
            if found is not None:
                results.append(company)
                break
   
   #  print(keywords_tokens_clean_stem)
   # #print(results)
   #  print("Description") 
   #  print(desp)
   #  print("Description Tokens")
   #  print(desp_tokens)
   #  print("Clean Tokens")
   #  print(desp_tokens_clean)
   #  print("Lemmatized Tokens")
   #  print(desp_tokens_clean_stem)
    with open(outfile, "w") as file_write:
        json.dump(results,file_write)
   
    
    
    return
if __name__ == "__main__":
    
    user_key = input("Enter the 32 digit user key: ")
    
    print("\nChoose from the following categories")
    print(get_categories())
    
    category = input("Enter the category chosen: ")
    
    outfile = input("Enter the name of the file to store results(eg: finance_results): ")
    outfile = outfile+".json"
    
    #user_key "d059f39b8f5fd5095490a564838fec8a"
    organizations = get_data("company", user_key)
    processor(organizations,category, outfile)
    
