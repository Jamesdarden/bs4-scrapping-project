from this import d
import pandas as pd
import numpy as np
import re
import sys

# file = pd.read_csv('supportlinkdata.csv')
# ['link', 'titleText', 'citeTag', 'caption']

# file['shady_score'] = int(0)


# print(file.dtypes)


def data_cleaning(x):

    regex_caption = re.compile(r'pc.?matic.*\d{3}.?\d{3}.?\d{4}|maticpc|pc.?matic.*\W{12}|pc.?matic.*number|pc.?matic.*support|pc.?matic.*tech',re.I)
    regex_link = re.compile(r'(pc[\w_-]?matic|\d{3}\w?\d|\W{3}\w?\d\W{4}).?support|[maticpc]{7}', re.I)
    regex_link_exclude = re.compile(r"review|bbb\.org|amazon\.com|pcpitstop\.com|linkedin\.com|pc\w?pitstop\.com|askbobrankin\.com|microsoft\.com|www\.facebook\.com/.?pcmatic/|tenforums\.com|article|news|[-_]vs[-_]|play\.google\.com|bleepingcomputer\.com|mozilla\.org|pinterest\.com|job|itqlick\.com|directory.siouxlandchamber.com|itqlick.com|dnb\.com|scamgaurd\.com|newegg\.com|ripoffreport\.com|folding\.extremeoverclocking\.com|findwhocallsyou\.com|y-hogey\.com|zoominfo\.com|thetop10sites\.com|404techsupport\.com|eabco\.net|shouldiremoveit\.com|facebook\.com\/pcmatic\/posts", re.I)
    regex_titleText = re.compile(r"pc.?matic.*\d{3}.?\d{3}.?\d{4}|pc.?matic|super.?shield",re.I)
    regex_caption_check= re.compile(r"pc.?matic.*\d{3}.?\d{3}.?\d{4}")
    shady_score = 0
    
    #helper function evalute expression return length of matches to assign score total
    def true_or_false (regex, row):
        return len(re.findall(regex, row ))
    
    
    if x.link:
        if  true_or_false(regex_link_exclude, str(x.link)):
        # if true_or_false(regex_link_exclude, x.link):
            if num := true_or_false(regex_caption_check, str(x.caption)):
                shady_score += num
            else:
                return 0
            
        elif num := true_or_false(regex_link, str(x.link)):
            
            shady_score +=  num
    if x.titleText :
        if num := true_or_false(regex_titleText, str(x.titleText)):
            shady_score += num
        
    if x.caption:
        if num := true_or_false(regex_caption, str(x.caption)):
    
            shady_score += num
    x.shady_score = shady_score 
    return x.shady_score



 

# file['shady_score'] = file.apply(data_cleaning, axis=1) #1 applyies to rows


# filtered_data = file[ file['shady_score'] > 0 ]


# filtered_data.to_csv("applied_style.csv")
# file.to_csv("applied_style2.csv")
# print(filtered_data)
# # print(len(file.index))