from GoogleScraper import scrape_with_config, GoogleSearchError
from GoogleScraper.database import ScraperSearch, SERP, Link

def searchongoogle(text, num):
    config = {
        'SCRAPING': {
            'use_own_ip': 'True',
            'keyword': text,
            'num_results_per_page': 50,
            'search_type': 'normal',
            'num_pages_for_keyword': int(num/10)*2,
            'offset':0,
            'search_engines': 'google'
        },
        'SELENIUM': {
            'sel_browser': 'chrome',
        },
        'GLOBAL': {
            'do_caching': 'False',
            'verbosity': 0
        }
    }
    try:
        sqlalchemy_session = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)
    linklist = []
    for s in sqlalchemy_session.serps:
        for link in s.links:
            l = str(link)[str(link).index('http'):str(link).__len__() - 1]
            if not linklist.__contains__(l):
                linklist.append(l)
    print('Founded ' + str(linklist.__len__()) + ' link on Google for: ' + text)
    return linklist
