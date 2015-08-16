import os
import sqlite3
import sys

from DHLib.TextMining import tag

def __initializeDB__(db):
    db.execute('''create table if not exists article_base (
       id integer primary key autoincrement,
       link text,
       parent integer);''')
    db.execute('''create table if not exists article (
       id integer primary key autoincrement,
       article_base_id integer,
       local_path text,
       title text,
       url text,
       tags text,
       data integer,
       is_base integer,
       foreign key (article_base_id) references article_base(id) on update cascade on delete cascade);''')

    db.execute('''create table if not exists image(
       id integer primary key autoincrement,
       article_id integer,
       local_path text,
       url text,
       size integer,
       foreign key (article_id) references article(id) on update cascade on delete cascade);''')

    db.execute('''create table if not exists comparated_image(
        article_base_id integer,
        img_base_id integer,
        img_base_path text,
        img_corr_id integer,
        img_corr_path text,
        SURFmin real,
        SURFmax real,
        correlation real,
        info text,
        is_similar integer,
        foreign key (img_base_id) references image(id) on update cascade on delete cascade,
        foreign key (img_corr_id) references image(id) on update cascade on delete cascade);''')


def __save_images_from_article__(ar):
    # download image
    from DHLib import workerpool

    #Initialize a pool, 5 threads
    pool = workerpool.WorkerPool(size=8)
    res = [im for im in pool.map(__download_image__, ar.images) if not im is None]
    pool.shutdown()
    pool.wait()
    return res


def __download_image__(data_link, path = 'cache/image/'):
    path = str(path)
    from urllib import request
    import xxhash
    # check if temp path exist
    if not os.path.exists(path):
        #make dir
        os.makedirs(path)
    #download and save file
    try:
        #download image data
        img_data = request.urlopen(data_link).read()
        #get image size
        img_size = sys.getsizeof(img_data)
        #check the size of an image
        if img_size > MIN_IMAGE_SIZE:
            #get the name
            img_name = str(xxhash.xxh64(img_data).hexdigest())
            f = open(path + img_name, 'wb')
            f.write(img_data)
            f.close()
        else:
            #the image is too small
            return None
    except:
        print(' - error for download: ' + str(data_link))
        return None
    return {'local_path': path + img_name, 'url': data_link, 'size': img_size}


def __save_article__(ar):
    # save into db
    #get data
    data = ar.publish_date
    if not data is None:
        #convert into UNIX time
        data = ar.publish_date.date().strftime("%s")

    #download text
    import xxhash

    f_title = 'cache/text/' + str(xxhash.xxh64(ar.text.encode('utf8')).hexdigest())
    f = open(f_title, 'w')
    f.write(ar.text)
    #TODO:Set the number of tag to be stored
    return {'local_path': f_title, 'title': ar.title, 'url': str(ar.url), 'tags': ' '.join(tag(ar.text, 10)), 'data': data}



def store_articles(article_base, context_articles, parent=0):
    # make directory structure
    if not os.path.exists('cache/text/'):
        os.makedirs('cache/text/')
    if not os.path.exists('cache/image/'):
        os.makedirs('cache/image')
    #connect database
    article_db = sqlite3.connect('cache/articles.db')
    #make table structure if not exist
    __initializeDB__(article_db)

    #save and store the base article
    result = __save_article__(article_base)

    article_db.execute('insert into article_base values(NULL,?,?)', [result['url'], str(parent)])
    #get the base article id
    article_base_id = article_db.execute('select id from article_base order by id desc limit 1;').fetchone()[0]

    #save the base article into database
    article_db.execute('insert into article values(NULL,?,?,?,?,?,?,?);',
                       [article_base_id, result['local_path'], result['title'], result['url'], result['tags'], result['data'], '1'])
    #get the images
    images_base = __save_images_from_article__(article_base)
    #get last article id
    last_article_id = article_db.execute('select id from article order by id desc limit 1;').fetchone()[0]

    #store base images into db
    for img in images_base:
        article_db.execute('insert into image values(NULL,?,?,?,?);',
                           [last_article_id, img['local_path'], img['url'], img['size']])

    for ar in context_articles:
        #save article
        result = __save_article__(ar)

        article_db.execute('insert into article values(NULL,?,?,?,?,?,?,?);',
                           [article_base_id, result['local_path'], result['title'], result['url'], result['tags'], result['data'], '0'])

        #get article id
        last_article_id = article_db.execute('select id from article order by id desc limit 1;').fetchone()[0]
        #get the images
        result = __save_images_from_article__(ar)
        #store into db
        for img in result:
            article_db.execute('insert into image (article_id, local_path, url, size) values (?,?,?,?);',
                               [last_article_id, img['local_path'], img['url'], img['size']])
    article_db.commit()
    article_db.close()
