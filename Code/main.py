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
N_TITLE = 120
#number of article to be downloaded by tags
N_TAG = 120
def main():
    #TODO: remove all file in cache
    if os.path.exists('cache'):
        import shutil
        #remove the previous cache file
        shutil.rmtree('cache')

    base_article_url = 'http://www.bbc.com/news/world-middle-east-31483631'
    base_article_url = 'http://www.bbc.com/news/world-europe-30765824'
    #load the first article
    base_article = Article(base_article_url)
    base_article.download()
    base_article.parse()
    article_title = base_article.title

    ####SEARCH FOR ARTICLE TITLE#######
    print('Searching article by title:'+ article_title)
    #get similar articles link without the base_article
    articles_by_title_link = [l for l in searchongoogle(article_title, N_TITLE) if l != base_article_url]

    #make parsed article list
    articles_by_title = article_list_from_link_list(articles_by_title_link)

    #####SEARCH FOR TAG########
    #join tag for doing the research
    tag_research = ' '.join(tag(base_article.text, 5))
    print('Tag researched: ', tag_research)
    #get article link searched by tag
    articles_by_tag_link = [l for l in searchongoogle(tag_research, N_TAG) if l != base_article_url]

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
    context_article = correlated_article(base_article, articles_by_title, articles_by_tag)
    print("Found " + str(context_article.__len__()) + " correlated article")
    
    print('Downloading and store file, this part can take several minutes ;)')
    ######STORE DATA#######
    ###MAKE DIRS STRUCTURE
    from ImageDownloader import download_image_from_article_list, download_data
    if not os.path.exists('cache/text/'):
        os.makedirs('cache/text/')
    if not os.path.exists('cache/image/'):
        os.makedirs('cache/image')

    ####DATABASE SECTION
    #make articles table
    import sqlite3
    article_db = sqlite3.connect('cache/articles.db')
    #article table
    article_db.execute('''create table article (
                        id integer primary key,
                        title text,
                        url text,
                        data integer)
                        ''')
    #image table
    article_db.execute('''create table image (
                        id integer primary key autoincrement,
                        article_id integer,
                        local_path text,
                        url text,
                        size integer,
                        allowed text
                        )''')
    #text table
    article_db.execute('''create table body (
                        id integer primary key autoincrement,
                        article_id integer,
                        local_path text,
                        tag text
                        )''')

    #TODO:get it better
    cont = -1
    #store the base article at position 0
    context_article = [base_article] + context_article
    for ar in context_article:
        cont += 1
        #save into db
        pb_date = ar.publish_date
        if not ar.publish_date == None:
            pb_date = ar.publish_date.date().strftime("%s")
        article_db.execute('insert into article values (?,?,?,?)',
                            [str(cont), str(ar.title), str(ar.url), str(pb_date)])

        #download image
        for img in ar.images:
            img_down_result = download_data(img, 'cache/image/')
            if not img_down_result == None:
                article_db.execute('insert into image values (NULL,?,?,?,?,?)',
                                    [str(cont), str(img_down_result[0]), str(img), str(img_down_result[1]), '0'])

        #download text
        import xxhash
        f_title = str(xxhash.xxh64(ar.text.encode('utf8')).hexdigest())
        f = open('cache/text/' + str(f_title), 'w')
        f.write(ar.text)
        #TODO : set the number of tag to be stored
        article_db.execute('insert into body values (NULL,?,?,?)',
                           [str(cont), "cache/text/" + str(f_title), ' '.join(tag(ar.text, 10))])
    article_db.commit()
    article_db.close()

if __name__ == '__main__':
    main()
