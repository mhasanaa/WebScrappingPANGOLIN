# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 21:13:44 2023

@author: Hasan
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import time
from datetime import datetime
start_time = time.process_time()
print("Start =", datetime.now().strftime("%H:%M:%S"))

## Input URL
URL = 'https://github.com/cov-lineages/pango-designation/issues'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
## Finding the class with reported issues
s = soup.find('div', class_='js-navigation-container js-active-navigation-container')
lines = s.find_all('a', href=True)
Report, Link = [], []
for line in lines:
    if 'S:' in line.text:
        Report.append(line.text)
        Link.append(line['href'])
print('Number of Reports: ',len(Report))
dfScrapping = pd.DataFrame({'Report':Report,'Link':Link})
dfScrapping['Link'] = ['https://github.com'+x for x in dfScrapping['Link']]
## Extracting sequence information
Info = ['-' if len(re.findall(r'\((.+)\)', sentence))==0 
        else '|'.join(re.findall(r'\(.+\)', sentence)) 
        for sentence in dfScrapping['Report'].tolist()]
dfScrapping['Info'] = Info
## Extracting variant
Variant = ['-' if len(re.findall(r'\D+\.\d\.*\d*\.*\d*',sentence))==0 
           else '|'.join(re.findall(r'\D+\.\d\.*\d*\.*\d*',sentence)) 
        for sentence in dfScrapping['Report'].tolist()]
dfScrapping['Variant'] = Variant
## Extracting spike mutations
Spikes = ['-' if len(re.findall(r'S:(\D\d+\D)',sentence))==0 
           else ','.join(re.findall(r'S:(\D\d+\D)',sentence)) 
        for sentence in dfScrapping['Report'].tolist()]
dfScrapping['Spikes'] = Spikes

print(dfScrapping)
dfScrapping.to_excel('Github.xlsx')
print("Current time =", datetime.now().strftime("%H:%M:%S"))
print('TIME TAKEN: ' + str(time.process_time() - start_time) + 's\n')