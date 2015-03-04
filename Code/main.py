import os
from newspaper import Article
#used for search on google
from DHLib.Searcher import searchongoogle
#used for find tag in a text
from DHLib.TextMining import tag
#used for select which article are in context
from DHLib.TextMining import correlated_article
from DHLib.StoreIntoDatabase import store_articles
#import constant
from Config import N_TAG, N_TITLE, C_N_TAG
from Config import ARTICLE_URL as article_base_url

def article_list_from_link_list(link_list):
    articles_list=[]
    for article_link in link_list:
        article = Article(article_link)
        article.download()
        try:
            article.parse()
            if article.text != '' and article.images.__len__()>0:
                #check if all link are images
                img_format =['jpg', 'png', 'bmp', 'jpeg']
                img_list = [i for i in article.images if i.split('.')[-1].lower() in img_format]
                article.images = img_list
                articles_list.append(article)
        except:
            print('error in article_list_from_link_list :' + article_link + ' is not an article')
    return articles_list


def main():
    if os.path.exists('cache'):
        import shutil
        #remove the previous cache file
        shutil.rmtree('cache')

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
    tag_research = ' '.join(tag(article_base.text, C_N_TAG))
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
    context_article = correlated_article(article_base, articles_by_title, articles_by_tag)
    print("Found " + str(context_article.__len__()) + " correlated article")

    print('Downloading and store file, this part can take several minutes ;)')

    #Download data and store into database
    store_articles(article_base, context_article)

    ######MATLAB PART FOR COMPARE
    from subprocess import call
    call(["matlab", "-nosplash -nodisplay -nojvm -r ImageCompare"]);

if __name__ == '__main__':
    main()
