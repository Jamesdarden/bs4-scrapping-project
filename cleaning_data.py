import pandas as pd
import numpy as np
import re
import sys

file = pd.read_csv('supportlinkdata.csv')
# ['link', 'titleText', 'citeTag', 'caption']

file['count_value'] = int(0)


# print(file.dtypes)


def data_cleaning(x):

    regex_caption = r'pc.?matic.*\d{3}.?\d{3}.?\d{4}|maticpc|pc.?matic.*\W{12}|pc.?matic.*number|support|tech'
    regex_link = r"pc[\w_-]?matic|[\d]{3}\w?[\d|\W]{3}\w?[\d\W]{4}|support|number"
    regex_link_exclude = r"review|bbb.org|amazon.com|pcpitstop.com|linkedin.com|pc\w?pitstop.com"
    # regex_caption = r'(pc.?matic).*\d{3}.?\d{3}.?\d{4}|maticpc|pc.?matic.*\W{12}|pc.?matic.*number|support|tech'
    # regex_link =r"(pc[\w_-]?matic)|[\d]{3}\w?[\d|\W]{3}\w?[\d\W]{4}|support|number"
    # regex_link_exclude = r"review|bbb.org|amazon.com|pcpitstop.com|linkedin.com|pc\w?pitstop.com"
    
    x.count_value = int(0)
    
    #helper function evalute expression return length of matches
    def true_or_false (regex, row):
        return len(re.findall(regex, row ,flags=re.I))
    
    
    

    
    if x.link:
        if re.compile(regex_link_exclude, x.link):
        # if true_or_false(regex_link_exclude, x.link):
            return int(x.count_value)
            
        if num := true_or_false(regex_link, x.link):
        # if num := true_or_false(regex_link, x.link):
            x.count_value = num
        
    if x.caption:
        if num := true_or_false(regex_caption, x.caption):
        # if num := true_or_false(regex_caption, x.link):
            x.count_value + num
    return x.count_value 
  
    # for col in x:
    #     if x.columns[col] == 'link':
    #         if re.compile(regex_link_exclude, x['link'], flags=re.I):
    #             x['count'] = None
    #         elif re.compile(regex_link, x['link'], flags=re.I):
    #             x['count'] +=1
    #     if x.columns[col] == 'caption':
    #         if re.compile(regex_caption, x['caption'], flags=re.I):
    #             x['count'] += 1
    #     else:
    #         return -1
    # for col in x.columns:
    # if re.compile(regex_link_exclude, x['link'], flags=re.I):
    #     return False
    # elif re.compile(regex_link, x['link'], flags=re.I):
    #     return True
    # elif re.compile(regex_caption, x['caption'], flags=re.I):
    #     return True
    # else:
    #     return False
    
 
flagcount = file[file.apply(data_cleaning, axis=1)] #1 applyies to rows
# # filtered_data = file['link'].filter(regex=regex_link).any(axis=1).to_string()
print(type(flagcount))
print(flagcount.head(), 'filtered data' )
# # print(len(file.index))