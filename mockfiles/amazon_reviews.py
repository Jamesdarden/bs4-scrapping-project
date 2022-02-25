import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

reviewlist = []
url = 'https://www.amazon.com/PreSonus-Studio-24c-USB-C-Interface/product-reviews/B07L9MWWDK/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
def getsoup(url):
    urls = 'https://www.amazon.com/PreSonus-Studio-24c-USB-C-Interface/product-reviews/B07L9MWWDK/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2'
    r = requests.get('http://localhost:8050/render.html',params={'url':url, 'wait':2})
    soup = BeautifulSoup(r.text,'html.parser')
    return soup
#print(soup.title.text) to  make sure we are getting the correct page.

def get_reviews(soup):
    reviews = soup.find_all('div',{'data-hook': 'review'})
    try:
        for item in reviews: 
            reviews ={
                'product': soup.title.text,
                'title': item.find('a',{'data-hook':'review-title'}).text.strip(),
                'rating':  float(item.find('i',{'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body':  item.find('span',{'data-hook': 'review-body'}).text.strip(),
                }
            reviewlist.append(reviews)
    except:
        pass
    
# python -i nameoffile brings up interactive  teeminal 
for x in range(1,10):
    soup = getsoup(f'https://www.amazon.com/PreSonus-Studio-24c-USB-C-Interface/product-reviews/B07L9MWWDK/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    get_reviews(soup)
    print(f'Getting page {x}')
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break
    
    df = pd.DataFrame(reviewlist)
    df.to_excel('presonus-review.xlsx',index=False)
    print('fin..')