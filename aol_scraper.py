
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib
import time
import os
from cleaning_data import data_cleaning

page = 0
supportList = []
suggestedTexts = set()
global_while_loop_counter =0
newList = []

def fetch_aol_results(url=None):
    global page
    global supportList
    global global_while_loop_counter
    global suggestedTexts
    global newList
    url_base = 'https://search.aol.com/aol/search/?q='
    suggestedLinks = {'"pc matic" assist number','"PC Matic" helpline number', '"pc matic" toll free number','"pc matic" tech support number'}
    if url :
        url = url
    else:
        url = url_base+'"pc+matic"+support+phone+number' 
    headers = { 'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
        'cache-control':'no-cache',
        'dnt':'1',
        'pragma':'no-cache',
        'referer':'https',
        'sec-fetch-mode':'no-cors',
        'sec-fetch-site':'cross-site',
        'Clear-Site-Data':"*",
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    #send to docker to render javascript
    r = requests.get('http://localhost:8050/render.html',params={'url':url,'wait':2}, headers=headers )
    
    
    soup = BeautifulSoup(r.text,'html.parser')
   
    #get related links
    related = soup.select('div.dd table.compTable tbody tr td')
    #get list of related urls to try
    if related:
        for item in related:
            #PC matic is not in the result added to make relevant search link
            item.text
            new_value = item.text
            if 'Related searches' in new_value:
                new_value = ''
            if 'pc matic' not in new_value:
                new_value = f'"pc matic" {new_value}'
            
            # new_value =[f'"pc matic" {x}' for x in new_value if 'pc matic' not in x]
            suggestedLinks.add(url_base +urllib.parse.quote_plus(new_value))
            suggestedTexts.add(item.text)
            
    
    
        
  
        
    #scrap search engine page gets all search results from page
    main_items = soup.select("div#web ol.searchCenterMiddle li div.dd.algo.algo-sr")
    
    #helper function to return unencoded link
    def returnReadableLink(item):
        string = item.find("a")['href']
        splitString = urllib.parse.unquote(string).split('https://')
        #remove empty values from string
        newstring = [x for x in splitString if len(x) > 0]
        # print(wanted_url[0])
        try:
            # print(newstring)
            regex_pattern = re.compile("(//)|(rk)", re.I)
            wanted_url = re.split(regex_pattern,newstring[1])
            print(wanted_url)
            newUrl = f'https://{wanted_url[0]}/'
            return newUrl
        except IndexError:
            # newUrl = splitString
            newUrl = string
            return newUrl
            
        
    
    for item in main_items:
        
        info ={   
            "link": returnReadableLink(item),
            "titleText" : item.find("h3", class_='title').text,
            "caption" :item.find("div",{"class":"compText"}).text
           
        }
        # add dict to list
      
        supportList.append(info)
 
     
    #making sure links don't contain pcmatic.com
    newDict =[d for d in supportList if 'pcmatic.com' not in d['link']]
    # print(newDict)
    #clearing support list
    supportList = []
      
    #cleaning data & writing data with a shadyscore of more than one        
    df = pd.DataFrame(newDict)
    if len(df.index) > 0:
        df['shady_score'] = df.apply(data_cleaning, axis=1)
        filtered_data = df[ df['shady_score'] > 0 ]
    else:
        filtered_data = df
        print('no dictionary items to add to csv')
    #check if values after cleaning
    if len(filtered_data.index) > 0:
        if os.path.exists('supportLinkData.csv') and os.path.getsize('supportLinkData.csv') > 0:
            value1 = pd.read_csv('supportLinkData.csv') 
            values = [value1, filtered_data]
            pd.concat(values, ignore_index=True).drop_duplicates(subset=['link'],keep='first',inplace=True).to_csv('supportLinkData.csv',index=False)
            print("writing to csv dictionary items")
        else:
            filtered_data.to_csv('supportLinkData.csv',index=False)
            print("writing to csv dictionary items")
           
        
    #clearing dataframes
    newDict.clear()
    print("wrote to csv file")
    
    
    
    
    people_also_searched_for = soup.find_all("div", {"class":"AlsoTry"})
    #extract the text elements from people_also_searched_for
    searched_for_list = [item.find("a").text for item in people_also_searched_for]
        
   
    # get other search terms
    if searched_for_list:
        df3 = pd.DataFrame( {'terms_searched':searched_for_list})
        if len(df3.index) > 0:
            if os.path.exists('peopelAlsoSearchedFor.csv') and os.path.getsize('peopelAlsoSearchedFor.csv') > 0:
                value2 = pd.read_csv('peopelAlsoSearchedFor.csv')
                values =[value2,df3]
                pd.concat(values, ignore_index=True).drop_duplicates().to_csv('peopelAlsoSearchedFor.csv',index=False)
            else:
                df3.to_csv('peopelAlsoSearchedFor.csv',index=False)
           
            searched_for_list.clear()
        print('wrote to search for csv')
       
    
    time.sleep(5)
    # #check if file exsist append if not write
    # if suggestedTexts:
    #     df2 = pd.DataFrame({'related_searches':list(suggestedTexts)})
    #     if os.path.exists('related_searches.csv') and os.path.getsize('related_searches.csv') > 0:
    #         value3= pd.read_csv('related_searches.csv')
    #         values= [df2,value3]
    #         pd.concat(values).drop_duplicates().to_csv('related_searches.csv', index=False)
            
    #     else:
    #         df2.to_csv('suggestions.csv',index=False)
            
    # # empty suggested text
    # suggestedTexts.clear()
        
    nextpage = soup.find('a',{'class': 'next'})['href']
    # print(nextpage, '+++++++==============')
    # scrap first 7 pages of search results
    if nextpage and page < 7:
        page += 1 
        print(f"page number in if statement {page} ")
        print('going through next page')
        fetch_aol_results(nextpage)
   
   
    # #initial search list
   
    # make set iterable by converting to list and preserve order
    # newList = list(suggestedLinks)
    
    
    addedList = [i for n, i in enumerate(suggestedLinks) if i not in newList]
    newList.extend(addedList)
    # go through first 15 suggestedlinks and scrap the the first 7 pages of each
    while global_while_loop_counter < len(newList) and global_while_loop_counter < 10:
        page = 0
        # print(global_while_loop_counter,"--------------------+++++++++++")
        # print(f"page number is {page} in while loop")
        print(f'this is the search term: {newList[global_while_loop_counter]}\nIn suggestlinks loop number : {global_while_loop_counter}')
        global_while_loop_counter += 1
        try:
            fetch_aol_results(url_base + urllib.parse.quote_plus(newList[global_while_loop_counter]))
        
        except IndexError:
            print(f"indexing error happened in yahoo scraper")
            break
    newList = []
        #suggestedlink scrap
        
        
    
   
    #add to main page 
    # print("done crawling yahoo")
    #initialize global variables to defaults 
    # global_while_loop_counter = 0 
    # page = 0
    # supportList = []
    # suggestedTexts = set()


fetch_aol_results()      
    
