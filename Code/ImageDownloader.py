import sqlite3
import os
import sys
from PIL import Image
#TODO:use the best MIN_IMAGE_SIZE
#minimum size of an image
MIN_IMAGE = 20000

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
        #get image size
        img_size = sys.getsizeof(img_data)
        #check the size of an image
        if img_size > MIN_IMAGE:
            #get the name
            img_name = str(xxhash.xxh64(img_data).hexdigest())
            f = open(path+img_name, 'wb')
            f.write(img_data)
            f.close()
        else:
            #the image is too small
            return None
    except:
        print('error for download: '+str(data_link))
        return None
    #return the image name
    #TODO:get the image's width and height
    img_width = 0
    img_height = 0
    return {
        'local_path': path+img_name,
        'url' : data_link,
        'size': img_size,
        'width': img_width,
        'height': img_height}

'''
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
'''
