from bing_scraper import fetch_bing_results
from yahoo_scraper import fetch_yahoo_results
from yandex_scraper import fetch_yandex_results
from aol_scraper import fetch_aol_results
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

def initialize_global_values_to_defaults(message):
    
    global page
    global global_while_loop_counter
    global suggestedTexts
    global supportList
    
    if isinstance(message,Exception):
        logger.exception(stack_info=True)
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
    initialize_global_values_to_defaults("Done crawling yandex")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yandex scraper:\n {e}")
try:
    fetch_yandex_results()
    initialize_global_values_to_defaults("Done crawling yandex")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yandex scraper:\n {e}")

    
print("done scrapping")
    

