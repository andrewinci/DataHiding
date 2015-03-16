#!/usr/local/bin/python3
import sqlite3
from urllib import request
import xxhash

db = sqlite3.connect('cache/articles.db');
imgs = [ a[0] for a in db.execute('select url from image')]

MIN_IMAGE_SIZE = 10
#download the images
for im_link in imgs:
    #download image data
    img_data = request.urlopen(im_link). read()
    #get the name
    img_name = str(xxhash.xxh64(img_data).hexdigest())
    f = open('cache/image/' + img_name, 'wb')
    f.write(img_data)
    f.close()
