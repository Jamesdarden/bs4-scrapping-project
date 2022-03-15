

import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib
import time
import os
from cleaning_data import data_cleaning
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)s - %(name)s - %(message)s')
stream_formatter = logging.Formatter('%(lineno)d - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('BingScraper.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

page = 0
supportList = []
suggestedTexts = set()
global_while_loop_counter =0
newList = []

def fetch_bing_results(url=None):
    global page
    global supportList
    global suggestedTexts
    global global_while_loop_counter
    global newList
    suggestedLinks = {'"pc matic" assist number','"PC Matic" helpline number', '"pc matic" toll free number','"pc matic" tech support number'}
    if url :
        url = url
    else:
        url = 'https://www.bing.com/search?q=contact+pc+matic+support+number&first=1&FORM=PERE' 
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
    try:
        
        r = requests.get('http://localhost:8050/render.html',params={'url':url,'wait':2}, headers=headers )
        soup = BeautifulSoup(r.text,'html.parser')
    except:
        logger.exception('exception occurred')
        
    
    
   
    #get related links
    related = soup.select('li.b_ans a[href]')
    if related:
        for item in related:
            if 'See all results for this question' in item or 'Feedback' in item or 'See all results for this question' in item or 'watch' in item or 'See more videos' in item:
                    related.remove(item)
        
    for link in related:
        suggestedLinks.add('https://www.bing.com/search?q='+urllib.parse.quote_plus(link.text))
        suggestedTexts.add(link.text)
    
    #scrap search engine page gets all search results from page
    items = soup.find_all('li',{'class':'b_algo'})
    for item in items:
        info ={   
            "link": item.find('a')['href'],
            "titleText": item.find('h2').text,
            "caption": item.find('div',{'class','b_caption'}).text
           
        }
        #add dict to list
      
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
        logger.info('no dictionary items to add to csv')
    #check if values after cleaning
    if len(filtered_data.index) > 0:
        if os.path.exists('supportLinkData.csv') and os.path.getsize('supportLinkData.csv') > 0:
            value1 = pd.read_csv('supportLinkData.csv') 
            values = [value1, filtered_data]
            pd.concat(values, ignore_index=True).drop_duplicates(subset=['link'],keep='first').to_csv('supportLinkData.csv',index=False)
            logger.info("writing to csv dictionary items")
        else:
            filtered_data.to_csv('supportLinkData.csv',index=False)
            logger.info("writing to csv dictionary items")
        
    #clearing dataframes
    newDict.clear()
    
    
    
    
    
    people_also_searched_for = soup.find_all('div', {'class':'b_expansion_text b_1linetrunc'})
    #get other search terms
    if people_also_searched_for:
        searched = [ x.text for x in people_also_searched_for]
        for item in range(0,len(searched)):
            if 'See all results for this question' in searched[item] or 'Feedback' in searched[item]:
                searched.remove(searched[item])
            
        df3 = pd.DataFrame( {'terms_searched':searched})
        if len(df3.index) > 0:
            if os.path.exists('peopelAlsoSearchedFor.csv') and os.path.getsize('peopelAlsoSearchedFor.csv') > 0:
                value2 = pd.read_csv('peopelAlsoSearchedFor.csv')
                values =[value2,df3]
                try:
                    pd.concat(values, ignore_index=True).drop_duplicates(subset='link',inplace=True, keep='first').to_csv('peopelAlsoSearchedFor.csv',index=False)
                except:
                    logger.exception('exception occurred')            
            else:
                df3.to_csv('peopelAlsoSearchedFor.csv',index=False)
           
            searched.clear()
        logger.info('wrote to search for csv')
       
    
    time.sleep(5)
    #check if file exsist append if not write
    if suggestedTexts:
        df2 = pd.DataFrame({'related_searches':list(suggestedTexts)})
        if os.path.exists('related_searches.csv') and os.path.getsize('related_searches.csv') > 0:
            value3= pd.read_csv('related_searches.csv')
            values= [df2,value3]
            pd.concat(values).drop_duplicates().to_csv('related_searches.csv', index=False)
            
        else:
            df2.to_csv('suggestions.csv',index=False)
            
    # empty suggested text
    suggestedTexts.clear()
        
    nextpage = soup.find('a',{'class': 'sb_pagN sb_pagN_bp b_widePag sb_bp'})['href']
    # print(nextpage, '+++++++==============')
    # scrap first 7 pages of search results
    if nextpage and page < 7:
        page += 1 
        parsed_url = urllib.parse.unquote_plus(urllib.parse.urlparse(url)[4])
        logger.info(f'going to page: {page}, in {parsed_url}')
        fetch_bing_results('https://www.bing.com/'+ nextpage)
   
   
    #initial search list
   
    # make set iterable by converting to list and keep order
    
    addedList = [i for n, i in enumerate(suggestedLinks) if i not in newList]
    newList.extend(addedList)

    
    # go through first 15 suggestedlinks and scrap the the first 7 pages of each
    while global_while_loop_counter < len(newList) and global_while_loop_counter < 10:
        page = 0
        logger.info(f'this is the search term: {newList[global_while_loop_counter]}\nIn suggestlinks loop number : {global_while_loop_counter}')
        global_while_loop_counter += 1
        try:
            fetch_bing_results('https://www.bing.com/search?q='+ urllib.parse.quote_plus(newList[global_while_loop_counter]))
        
        except:
            logger.exception('exception occurred')
        #suggestedlink scrap  
            break 
    newList =[]
    #initialize global variables to defaults 
    # global_while_loop_counter = 0 
    # page = 0
    # supportList = []
    # suggestedTexts = set()
    # print("done crawling bing")


fetch_bing_results()      
    
