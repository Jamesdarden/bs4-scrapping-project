import requests
import csv
import  pandas as pd
import concurrent.futures
# proxy = '164.100.130.128:8080'
# r = requests.get('https://httpbin.org/ip', proxies={'http':proxy,'https':proxy,}, timeout=3)

# print(r.status_code)

proxielist = []

with open('proxies.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        proxielist.append(row[3])
        
workingList = []
def extract(proxy):
    try:
        r =requests.get('http://httpbin.org/ip', proxies={'http':proxy , 'https':proxy},timeout=2)
        print(r.json(), ' - working')
        workingList.append(proxy)
    except:
        pass
    return proxy

# with concurrent.futures.ThreadPoolExecutor(max_workers=25) as exector:
#     exector.map(extract, proxielist )



df =pd.DataFrame(workingList)
df.to_csv('workingList.csv', index=False)
