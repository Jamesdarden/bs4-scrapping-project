
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from cleaning_data import data_cleaning
import pandas as pd
import os
import time
import urllib
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

global_while_loop_counter =0
supportList = []
page = 0




#send to docker to render javascript
# url = 'https://yandex.com/search/?text="pc+matic"+support+number&lr=87&redircnt=1646431681.1'



# div.main-content
def get_soup(url):
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
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page =browser.new_page(extra_http_headers=headers)
        page.goto(url)
        # page.fill(input#imput, textToBeUsed) uses css selectors selects element and fills with text 
        # page.is_visible()
        page.wait_for_load_state(state='domcontentloaded')
        if page.is_visible('input[type=submit]'):
            page.click('input[type=submit]')
        if page.is_visible("div.CheckboxCaptcha-Checkbox"):
            page.locator("text=Accept").click()
        page.wait_for_selector("div.content__left")
        html = page.inner_html("div.content__left")
        soup = BeautifulSoup(html,'html.parser')
        page.close()
    return soup
def fetch_yandex_results(url=None):
    global global_while_loop_counter
    global supportList
    global page
    
    # suggestedLinks = ['"pc matic" assist number','"PC Matic" helpline number', '"pc matic" toll free number','"pc matic" tech support number','How do I contact "pcmatic" customer support','Is there a "PC Matic" technical support company']
    suggestedLinks = ['"PC Matic" helpline number', '"pc matic" toll free number','"pc matic" tech support number','How do I contact "pcmatic" customer support','Is there a "PC Matic" technical support company']
    
    if not url:
        url = 'https://yandex.com/search/?text="pc+matic"+assist+number'
    
    #parsed html elements
    try:
        soup =  get_soup(url)
    except:
        logger.exception('exception occurred')
        
   
    items = soup.select("li.serp-item.desktop-card")
    for item in items:
        info ={
            "link": item.find("a")["href"],
            "titleText":item.select_one("h2.OrganicTitle-LinkText").text,
            "caption": item.select_one("div.Organic-ContentWrapper").text
        }
        supportList.append(info)
    #make sure PC Matic not in support list
    newDict = [d for d in supportList if 'pcmatic.com' not in d['link']] 

    supportList = []
    
    #cleaning data & writing data with a shadyscore of more than one        
    df = pd.DataFrame(newDict)
    if len(df.index) > 0:
        df['shady_score'] = df.apply(data_cleaning, axis=1)
        filtered_data = df[ df['shady_score'] > 0 ]
    else:
        filtered_data = df
        logger.warning('no dictionary items to add to csv')
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

    newDict.clear()
    time.sleep(120)

    next_page = soup.select_one("div.pager div.pager__items a.pager__item_kind_next")['href']
    next_page_link ='https://yandex.com/'+next_page
    
   
    if next_page_link and page < 2:
        page += 1
        parsed_url = urllib.parse.unquote_plus(urllib.parse.urlparse(url)[4])
        logger.info(f'going to page: {page}, in {parsed_url}')
        fetch_yandex_results(next_page_link)
    

        
    while global_while_loop_counter < len(supportList) and global_while_loop_counter < 6:
        
        page = 0
        logger.info(f"Searching next term: {suggestedLinks[global_while_loop_counter]}")
        global_while_loop_counter += 1
        try:
            fetch_yandex_results('https://yandex.com/search/?text=' + urllib.parse.quote_plus(suggestedLinks[global_while_loop_counter], safe="/"))
        except:
            logger.exception('exception occurred')

        

fetch_yandex_results()   