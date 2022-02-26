import pandas as pd
import numpy as np
import re
import sys

file = pd.read_csv('supportlinkdata.csv')
# ['link', 'titleText', 'citeTag', 'caption']

file['count_value'] = int(0)


# print(file.dtypes)


def data_cleaning(x):

    regex_caption = re.compile(r'pc.?matic.*\d{3}.?\d{3}.?\d{4}|maticpc|pc.?matic.*\W{12}|pc.?matic.*number|support|tech',re.I)
    regex_link = re.compile(r'pc\[\w_-\]?matic|\d{3}\w?\d|\W{3}\w?\d\W{4}|support|number', re.I)
    regex_link_exclude = re.compile(r"review|bbb.org|amazon.com|pcpitstop.com|linkedin.com|pc\w?pitstop.com", re.I)
    count_value = 0
    
    #helper function evalute expression return length of matches
    def true_or_false (regex, row):
        return len(re.findall(regex, row ))
    
    
    if x.link:
        if regex_link_exclude.search(x.link):
        # if true_or_false(regex_link_exclude, x.link):
            return 0
            
        elif num := true_or_false(regex_link, x.link):
        # if num := true_or_false(regex_link, x.link):
            count_value +=  num
        
    if x.caption:
        if num := true_or_false(regex_caption, x.caption):
        # if num := true_or_false(regex_caption, x.link):
            count_value += num
    x.count_value = count_value 
    return x.count_value
  
   
 
# flagcount = file['count_value'][file.apply(data_cleaning, axis=1)] #1 applyies to rows
file['count_value'] = file.apply(data_cleaning, axis=1) #1 applyies to rows
# # filtered_data = file['link'].filter(regex=regex_link).any(axis=1).to_string()
# print(type(flagcount))
filtered_data = file[ file['count_value'] > 0 ]
# print(filtered_data)
filtered_data.to_csv("filtered_data.csv")
# # print(len(file.index))