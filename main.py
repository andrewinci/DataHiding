__author__ = 'darka'
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
                img_list = [i for i in article.images if i.split('.')[-1] in img_format]
                article.images = img_list
                #TODO:Remove
                print('Date is present :' + str(article.publish_date))
                articles_list.append(article)
        except:
            print('error in article_list_from_link_list :' + article_link + ' is not an article')
    return articles_list


def main():
    #TODO: remove all file in cache
    base_article_url = 'http://www.bbc.com/news/world-middle-east-31483631'
    base_article_url = 'http://www.bbc.com/news/world-europe-30765824'
    #load the first article
    base_article = Article(base_article_url)
    base_article.download()
    base_article.parse()
    article_title = base_article.title

    ####SEARCH FOR ARTICLE TITLE
    print('Searching article by title:'+ article_title)
    #get similar articles link without the base_article
    articles_by_title_link = [l for l in searchongoogle(article_title, 10) if l != base_article_url]

    #make parsed article list
    articles_by_title = article_list_from_link_list(articles_by_title_link)

    #####SEARCH FOR TAG
    #join tag for doing the research
    tag_research = ' '.join(tag(base_article.text, 5))
    print('Tag researched: ', tag_research)
    #get article link searched by tag
    articles_by_tag_link = [l for l in searchongoogle(tag_research, 10) if l != base_article_url]

    #make parsed article list
    articles_by_tag = article_list_from_link_list(articles_by_tag_link)
    '''
    #####SELECT THE RESULTS
    #simple intersection between them
    intersection = [ar for ar in articles_by_tag_link if articles_by_title_link.__contains__(ar)]
    print('There is '+ str(intersection.__len__()) + ' link in the intersection')
    for article_link in intersection:
            print(article_link)
    #using a TextCompare
    import TextCompare
    TextCompare.MAX=1
    TextCompare.MIN=0
    context_article = articles_by_title + [ar for ar in articles_by_tag if TextCompare.is_article_in_context(ar, articles_by_title)]
    '''
    #download context images and store into db
    from ImageDownloader import download_image_from_article_list
    download_image_from_article_list(articles_by_title+articles_by_tag, 'img.db', 'context_images')

    #download base images and store into db
    download_image_from_article_list([base_article], 'img.db', 'base_images')

    #TODO:Compare image, fix similitude alghoritm
    import sqlite3
    from ImageCompare import compare
    db = sqlite3.connect('.imagecache/img.db')
    base_images = db.execute('select * from base_images').fetchall()
    context_images = db.execute('select * from context_images').fetchall()
    #create a similitude table
    db.execute("create table similitude_table (id integer primary key autoincrement, img_base_id integer, simil real, img_context_id integer);")
    print('Calculating the similitude.....')
    for b in base_images:
        for c in context_images:
            #compute similitude
            try:
                sim_value = compare(b[2], c[2])
                db.execute('insert into similitude_table values (NULL,' + str(b[0]) + ',' + str(sim_value) + ',' + str(c[0]) + ');')
            except:
                print('Error in :' + str(b[2]) + "," + str(c[2]))
    db.commit()
    db.close()

if __name__ == '__main__':
    main()