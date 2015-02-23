import sqlite3
db = sqlite3.connect('.imagecache/img.db')
MIN = 90
MAX = 100
simil_img = db.execute("select * from similitude_table where simil <= "+str(MAX)+" and simil >= "+str(MIN)).fetchall()
for s in simil_img:
    img_base = db.execute("select * from base_images where id = "+str(s[1])).fetchone()
    img_context  = db.execute("select * from context_images where id = "+ str(s[3])).fetchone()
    print(img_base[1], str(s[2]), img_context[1])
db.close()

from datetime import datetime
