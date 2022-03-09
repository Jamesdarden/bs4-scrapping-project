from bing_scraper import fetch_bing_results
from yahoo_scraper import fetch_yahoo_results
from yandex_scraper import fetch_yandex_results


page = 0
supportList = []
suggestedTexts = set()
global_while_loop_counter =0

def initialize_global_values_to_defaults(message):
    
    global page
    global global_while_loop_counter
    global suggestedTexts
    global supportList
    print(f"{message}")
   
    global_while_loop_counter = 0 
    page = 0
    supportList = []
    suggestedTexts = set()
    



try:
    fetch_bing_results()
    initialize_global_values_to_defaults("Done crawling bing")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong Bing scraper:\n {str(e)}")
try:
    fetch_yahoo_results()
    initialize_global_values_to_defaults("Done crawling yahoo")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yahoo scraper:\n {str(e)}")
    
initialize_global_values_to_defaults("Yahoo")
try:
    fetch_yandex_results()
    initialize_global_values_to_defaults("Done crawling yandex")
except Exception as e:
    initialize_global_values_to_defaults(f"something went wrong yandex scraper:\n {str(e)}")

    
print("done scrapping")
    

