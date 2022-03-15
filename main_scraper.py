from bing_scraper import fetch_bing_results
from yahoo_scraper import fetch_yahoo_results
from yandex_scraper import fetch_yandex_results
from aol_scraper import fetch_aol_results
import logging
import pandas as pd
import re

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

def initialize_global_values_to_defaults(message):
    
    global page
    global global_while_loop_counter
    global suggestedTexts
    global supportList
    
    if isinstance(message,Exception):
        logger.exception('exception occurred')
    else:
        logger.info(message)
    
   
    global_while_loop_counter = 0 
    page = 0
    supportList = []
    suggestedTexts = set()
    



try:
    fetch_bing_results()
    initialize_global_values_to_defaults("Done crawling bing")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong Bing scraper:\n {e}")
try:
    fetch_yahoo_results()
    initialize_global_values_to_defaults("Done crawling yahoo")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yahoo scraper:\n {e}")
    
initialize_global_values_to_defaults("Yahoo")
try:
    fetch_aol_results()
    initialize_global_values_to_defaults("Done crawling aol")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yandex scraper:\n {e}")
try:
    fetch_yandex_results()
    initialize_global_values_to_defaults("Done crawling yandex")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yandex scraper:\n {e}")

    
logger.info("done scrapping")


file = pd.read_csv(".supportLinkData_copy.csv")



def fix_url(url):
    pattern = re.compile('(\/RK=2)|(\/\/RK=2)')
    pattern2 = re.compile('\/\/$')
    pattern3 = re.compile('www.www.',re.I)
    newString = str(url)
    
    if re.search(pattern,str(newString)):
        newString = re.split(pattern, newString)[0]+'/'
    if re.search(pattern2,str(newString)):
        newString = re.sub(pattern2, "/", newString)
    if re.search(pattern3, str(newString)):
        newString = re.sub(pattern3,'www.', newString)
    if string :=list(newString)[-1:] == '/':
        newString = ''.join(string[0:-1])
        
    return str(newString).strip()

#running function on column populating values in temp list
newList = [[fix_url(x) for x in file['link']]]
#changing list to dataFrame and seperaing list items
newUlrDf = pd.DataFrame({'link':x for x in newList})
#dropping previoul list column
file.drop(columns=['link'],axis=1,inplace=True)
#then adding new link column to DF
file['link'] = newUlrDf
#adding link column to index 0 of dataframe
cols = ['link','titleText', 'caption', 'shady_score']
file = file[cols]
#dropping duplicates
file= file.drop_duplicates(subset=['link','caption'],keep='first').reset_index(drop=True).sort_values(by=['shady_score','link'])

file.to_csv('cleaned_data.csv', index=False)
    

