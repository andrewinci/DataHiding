import os
from newspaper import Article
from Tagger import tag
from Searcher import searchongoogle


def article_list_from_link_list(link_list):
    articles_list=[]
    for article_link in link_list:
        article = Article(article_link)
        article.download()
        try:
            article.parse()
            if article.text != '' and article.images.__len__()>0:
                #check if all file in images are really image
                img_format =['jpg', 'png', 'bmp', 'jpeg']
                img_list = [i for i in article.images if i.split('.')[-1].lower() in img_format]
                article.images = img_list
                articles_list.append(article)
        except:
            print('error in article_list_from_link_list :' + article_link + ' is not an article')
    return articles_list


#number of article to be downloaded by title
N_TITLE = 10
#number of article to be downloaded by tags
N_TAG = 10


def main():
    #TODO: remove all file in cache
    if os.path.exists('cache'):
        import shutil
        #remove the previous cache file
        shutil.rmtree('cache')

    article_base_url = 'http://www.bbc.com/news/world-middle-east-31483631'
    article_base_url = 'http://www.bbc.com/news/world-europe-30765824'
    #load the first article
    article_base = Article(article_base_url)
    article_base.download()
    article_base.parse()
    article_title = article_base.title

    ####SEARCH FOR ARTICLE TITLE#######
    print('Searching article by title:'+ article_title)
    #get similar articles link without the article_base
    articles_by_title_link = [l for l in searchongoogle(article_title, N_TITLE) if l != article_base_url]

    #make parsed article list
    articles_by_title = article_list_from_link_list(articles_by_title_link)

    #####SEARCH FOR TAG########
    #join tag for doing the research
    tag_research = ' '.join(tag(article_base.text, 5))
    print('Tag researched: ', tag_research)
    #get article link searched by tag
    articles_by_tag_link = [l for l in searchongoogle(tag_research, N_TAG) if l != article_base_url]

    #make parsed article list
    articles_by_tag = article_list_from_link_list(articles_by_tag_link)

    #####SELECT THE RESULTS#######
    #simple intersection between them
    intersection = [ar for ar in articles_by_tag_link if articles_by_title_link.__contains__(ar)]
    print('There is '+ str(intersection.__len__()) + ' link in the intersection')
    for article_link in intersection:
            print(article_link)

    #using a TextCompare
    from TextCompare import correlated_article
    context_article = correlated_article(article_base, articles_by_title, articles_by_tag)
    print("Found " + str(context_article.__len__()) + " correlated article")

    print('Downloading and store file, this part can take several minutes ;)')

    from StoreIntoDatabase import store_articles
    store_articles(article_base, context_article)

if __name__ == '__main__':
    main()
