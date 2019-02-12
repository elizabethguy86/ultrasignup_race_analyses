import requests
from selenium.webdriver import (Chrome)
import pandas as pd
import numpy as np

class Get_ultrasignup_data():
    '''class to take in a webpage from ultrasignup
    and return a dataframe of finish times (in mins)
    for males and females.  Dataframe contains gender
    and finish time.'''
    
    def __init__(self, url):
        self.url = url
    
    def find_idx(self, content):
        '''finds the index for the DNF and DNS sublists 
        from the larger scraped results.'''
        indices = []
        for idx, row in enumerate(content):
            if row[0] == 'Did':
                indices.append(idx)
    return indices
    
    def scrape_results(self):
         '''Starts web scraper to get table
        with runner results.  Returns column headers
        and result data.'''
        browser = Chrome()
        browser.get(self.url)
        sel = "gbox_list" 
        cascade100results=browser.find_element_by_id(sel) #setting a css selector
        table_rows = cascade100results.text.split('\n')
        runner_rows = [row.split() for row in table_rows]
        self.cols = runner_rows[0:10] #column headers
        self.content = runner_rows[11:] #the actual runner results
        self.idx = self.find_idx(self.content)
        return (self.cols, self.content, self.idx)
    
    def make_finisher_df():
        '''take in runner row content and the index
        indicating the end of the finishers list (idx_1).  
        return dataframe with the male and female times.'''
        cols, content, idx = self.scrape_results()
        finished = content[0:idx[0]]
        gender = []
        times = []
        for row in finished:
            times.append(row[-2])
            gender.append(row[-4])
        df = pd.DataFrame({'Gender': gender, 'Time': times})
        df['Time'] = df['Time'].str.split(':')
        df['Time'] = df['Time'].apply(lambda x: int(x[0]) * 60 + int(x[1]) + float(x[2])/60)
        return df
        
    