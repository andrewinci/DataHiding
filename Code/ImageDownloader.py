import sqlite3
import os
import sys

'''
path of the form bla/bla/
'''
def download_data(data_link, path):
    path=str(path)
    from urllib import request
    import xxhash
    #check if temp path exist
    if not os.path.exists(path):
        #make dir
        os.makedirs(path)
    #download and save file
    try:
        #download image data
        img_data = request.urlopen(data_link).read()
        #check the size of an image
        if sys.getsizeof(img_data) > 20000:
            #get the name
            img_name = str(xxhash.xxh64(img_data).hexdigest())
            f = open(path+img_name, 'wb')
            f.write(img_data)
            f.close()
        else:
            #print('too small')
            return None
    except:
        print('error for download: '+str(data_link))
        return None
    #return the image name
    return path+ img_name


def download_image_from_article_list(article_list, db_name, table_name):
    #check if db already exist
    # #create db
    db = sqlite3.connect('.imagecache/'+db_name)
    #TODO:fix if file is present
    #create table
    db.execute("create table " + table_name + " (id integer primary key autoincrement, img_link text, img_path text, article_link text)")
    for ar in article_list:
        article_link = ar.canonical_link
        #downlad images
        for img_link in ar.images:
            img_path = download_data(img_link, '.imagecache/')
            #adding img to database
            if img_path != None:
                db.execute("insert into " + table_name + " values (NULL,\'"+str(img_link)+'\',\''+str(img_path)+'\',\''+ str(article_link)+'\');')
    db.commit()
    db.close()