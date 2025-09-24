import Model as Model
from bs4 import BeautifulSoup
import scraper as scraper

def Engine(prompt):
    
    web_list = Model.Model(prompt,5)
            
    raw_data = []
    
    for i in web_list:
        raw_data.append(scraper.dynamic_scrape(i))
        
    data = Model.DataModel(raw_data)
    
    return data