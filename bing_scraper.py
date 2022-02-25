from numpy import delete
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib
import time
import os

page = 0
supportList = []
suggestedLinks = set()
suggestedTexts = set()

def fetch_url(url=None):
    global page
    global supportList
    if url :
        url = url
    else:
        url = 'https://www.bing.com/search?q=contact+pc+matic+support+number&first=1&FORM=PERE' 
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
    r = requests.get('http://localhost:8050/render.html',params={'url':url,'wait':2}, headers=headers )
    soup = BeautifulSoup(r.text,'html.parser')
    related = soup.select('li.b_ans a[href]')
    for link in related:
        suggestedLinks.add('https://www.bing.com'+str(link))
        suggestedTexts.add(link.text)
    
    items = soup.find_all('li',{'class':'b_algo'})
    #print(soup.find('li',{'class':'b_algo'}))
    # print(items.find('cite').text)
    for item in items:
        info ={   
            "link": item.find('a')['href'],
            "titleText": item.find('h2').text,
            "citeTag": item.find('cite').text,
            "caption": item.find('div',{'class','b_caption'}).text
        }
        supportList.append(info)
    #making sure links don't contain pcmatic.com
    newDict =[d for d in supportList if 'pcmatic.com' not in d['link']]
    supportList = []
            
    df = pd.DataFrame(newDict)
    if os.path.exists('supportLinkData.csv') and os.path.getsize('supportLinkData.csv') > 0:
        pd.read_csv('supportLinkData.csv').append(df).drop_duplicates(subset=['link'],keep='first').to_csv('supportLinkData.csv', index=False)

    else:
        df.to_csv('supportLinkData.csv', index=False)
        
    #clearing new  dict
  
    print("writing to csv dictionary items")
    
    
    
    people_also_searched_for = soup.find_all('div', {'class':'b_expansion_text b_1linetrunc'})
    if people_also_searched_for:
        searched = [ x.text for x in people_also_searched_for]
        df3 = pd.DataFrame(list(searched))
        if os.path.exists('peopelAlsoSearchedFor.csv') and os.path.getsize('peopelAlsoSearchedFor.csv') > 0:
            pd.read_csv('peopelAlsoSearchedFor.csv').append(df3).drop_duplicates().to_csv('peopelAlsoSearchedFor.csv', index=False)
        else:
            df3.to_csv('peopelAlsoSearchedFor.csv')
        
        print('wrote to search for csv')
       
    
    time.sleep(5)
    
    if os.path.exists('peopelAlsoSearchedFor.csv') and os.path.getsize('peopelAlsoSearchedFor.csv') > 0:
        df2 = pd.DataFrame(suggestedTexts)
        pd.read_csv('suggestions.csv').append(df2).drop_duplicates().to_csv('suggestions.csv', index=False)
    else:
        df2 = pd.DataFrame(suggestedTexts)
        df2.to_csv('suggestions.csv',index=False)
        
    nextpage = soup.find('a',{'class': 'sb_pagN sb_pagN_bp b_widePag sb_bp'})['href']
    # print(nextpage, '+++++++==============')
    if nextpage and page < 10:
        page += 1 
        print('going through next page')
        fetch_url('https://www.bing.com/'+ nextpage)
    else:
        searchTerms = ['"pc matic" assist number','"PC Matic" helpline number', '"pc matic" toll free number','"pc matic" tech support number']
        page = 0
       
        for i in range(0, len(searchTerms)):
            print(f'this is the search term: {i} {searchTerms[i]}')
            fetch_url('https://www.bing.com/search?q='+ urllib.parse.quote_plus(searchTerms[i]))


fetch_url()      
    
