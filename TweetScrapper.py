# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:13:01 2017
@author: kishi
----Update----
Creted Wed Jan 22 15:41 2020
@Edited: Konstmann
"""

from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests


def tweet(url):

    browser = requests.get(url)

    return browser.text


#function to handle/parse HTML and extract data - using BeautifulSoup    
def scrapper(url):
    
    #regex patterns
    url_finder = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    problemchars = re.compile(r'[\[=\+/&<>;:!\\|*^\'"\?%$@)(_\,\.\t\r\n0-9-—\]]')
    # Date and time formate string
    dateFormat = '%H.%M - %d. %b. %Y'
 
    blog_list = []  
    
    #call dynamic page scroll function here
    soup = BeautifulSoup(tweet(url), "html.parser")
    
    for i in soup.find_all('li', {"data-item-type":"tweet"}):
        link = ('https://twitter.com' + i.small.a['href'] if i.small is not None else "")
        date = (i.small.a['title'] if i.small is not None else "")
        text = (i.p.get_text().replace('\n','') if i.p is not None else "")

        if date.count(".") == 3: # Some dates misses a dot after month, discard if not there
            #build dictionary to format data as key-pair value 
            blog_dict = {
            "url": link,
            "date": datetime.strptime(date, dateFormat),
            #before text is stored URLs are removed - note: hash symbol is maintained to indicate hashtag term
            "blog_text": problemchars.sub(' ', url_finder.sub('', text))
            }
            
            blog_list.append(blog_dict)            
    
    return blog_list

    
#main
if __name__ == "__main__":
    scrapper("https://twitter.com/OculusSupport")