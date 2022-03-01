from numpy import delete, not_equal
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

def fetch_bing_results(url=None):
    global page
    global supportList
    suggestedLinks = {'"pc matic" assist number','"PC Matic" helpline number', '"pc matic" toll free number','"pc matic" tech support number'}
    if url :
        url = url
    else:
        url = 'https://www.bing.com/search?q=contact+pc+matic+support+number&first=1&FORM=PERE' 
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
    #send to docker to render javascript
    r = requests.get('http://localhost:8050/render.html',params={'url':url,'wait':2}, headers=headers )
    
    
    soup = BeautifulSoup(r.text,'html.parser')
   
    #get related links
    related = soup.select('li.b_ans a[href]')
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
    df['shady_score'] = df.apply(data_cleaning, axis=1)
    filtered_data = df[ df['shady_score'] > 0 ]
    #check if values after cleaning
    if len(filtered_data.index) > 0:
        if os.path.exists('supportLinkData.csv') and os.path.getsize('supportLinkData.csv') > 0:
            pd.read_csv('supportLinkData.csv').append(filtered_data).drop_duplicates(subset=['link'],keep='first').to_csv('supportLinkData.csv')
            del filtered_data
            del df
        else:
            filtered_data.to_csv('supportLinkData.csv')
            del filtered_data
            del df
        
    #clearing dataframes
    newDict.clear()
    
    print("writing to csv dictionary items")
    
    
    
    people_also_searched_for = soup.find_all('div', {'class':'b_expansion_text b_1linetrunc'})
    #get other search terms
    if people_also_searched_for:
        searched = [ x.text for x in people_also_searched_for]
        for item in range(0,len(searched)):
            if 'See all results for this question' in searched[item] or 'feedback' in searched[item]:
                searched.remove(searched[item])
            
        df3 = pd.DataFrame(searched)
        if len(df3.index) > 0:
            if os.path.exists('peopelAlsoSearchedFor.csv') and os.path.getsize('peopelAlsoSearchedFor.csv') > 0:
                pd.read_csv('peopelAlsoSearchedFor.csv').append(df3).drop_duplicates().to_csv('peopelAlsoSearchedFor.csv')
            else:
                df3.to_csv('peopelAlsoSearchedFor.csv')
            del df3
            searched.clear()
        print('wrote to search for csv')
       
    
    time.sleep(5)
    #check if file exsist append if not write
    if suggestedTexts:
        if os.path.exists('suggestions.csv') and os.path.getsize('suggestions.csv') > 0:
            df2 = pd.DataFrame(suggestedTexts)
            pd.read_csv('suggestions.csv').append(df2).drop_duplicates().to_csv('suggestions.csv')
            del df2
        else:
            df2 = pd.DataFrame(suggestedTexts)
            df2.to_csv('suggestions.csv')
            del df2
    # empty suggested text
    suggestedTexts.clear()
        
    nextpage = soup.find('a',{'class': 'sb_pagN sb_pagN_bp b_widePag sb_bp'})['href']
    # print(nextpage, '+++++++==============')
    if nextpage and page < 8:
        page += 1 
        print('going through next page')
        fetch_bing_results('https://www.bing.com/'+ nextpage)
    else:
        #initial search list
     
        page = 0
       
        for count, item in enumerate(suggestedLinks, start=0):
            if count == 25:
                break
            print(f'this is the search term: {item}\nIn suggestlinks loop')
            fetch_bing_results('https://www.bing.com/search?q='+ urllib.parse.quote_plus(item))
            #suggestedlink scrap    
            
        print("done crawling bing")


fetch_bing_results()      
    
