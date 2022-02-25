import requests
from bs4 import BeautifulSoup
import re


questionList = []
def get_questions(tag, page):
    
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
    url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=active&page={page}&pagesize=30'
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    soup =BeautifulSoup(r.text, 'html.parser')
    # print(soup.title.text)
    questions = soup.find_all('div',{'class':'s-post-summary js-post-summary'})
    # print(len(questions))
    for item in questions:
    
        question = {
        'title' : item.find('h3',{'class':'s-post-summary--content-title'}).text,
        'link' : 'https://stackoverflow.com'+item.find('a',{'class':'s-link'})['href'],
        'votes' : int(item.find('span',{'class':'s-post-summary--stats-item-number'}).text),
        'date' : item.find('span',{'class':'relativetime'})['title'],
        }
        questionList.append(question)
    
for x in range(1,3):
    get_questions('python', x)
    get_questions('flask', x)
    
print(len(questionList))
    
    
    
