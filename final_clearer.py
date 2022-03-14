import pandas as pd
import numpy as np
import re

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