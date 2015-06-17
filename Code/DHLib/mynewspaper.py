__author__ = 'darka'

import requests
from newspaper import Article
from bs4 import BeautifulSoup


def gettext(url):
    uri = 'http://newspaper-demo.herokuapp.com/articles/show?url_to_clean='+url
    response = requests.get(uri)

    bs = BeautifulSoup(response.content)
    fields = [str(f).replace('<td>','').replace('</td>','') for f in bs.find_all('td')]
    text = fields[fields.index('Text')+1]
    #print(text)
    return text
