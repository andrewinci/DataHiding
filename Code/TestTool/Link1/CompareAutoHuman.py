#!/usr/local/bin/python3
import sqlite3

humandb = sqlite3.connect('cache/articles.db')
autodb = sqlite3.connect('articles.db')

query = '''select
    comparated_image.is_similar,
    image_base.url,
    image_corr.url
    from comparated_image
    inner join image as image_base on image_base.id = comparated_image.img_base_id
    inner join image as image_corr on image_corr.id = comparated_image.img_corr_id
'''

humansim = humandb.execute(query).fetchall()
autosim = autodb.execute(query).fetchall()

f= open('ha.html','w')

ok = 0;
no = 0;
nc = 0;
for a in humansim:
    for b in autosim:
        if a[1] == b[1] and a[2] == b[2]:
            if b[0]==2:
                nc+=1
            elif a[0]==b[0]:
                ok+=1
            else:
                #write in command line
                print('\nhuman sim:'+str(a[0])+' base:'+str(a[1])+' corr:'+str(a[2]))
                print('auto sim:'+str(b[0])+' base:'+str(b[1])+' corr:'+str(b[2]))
                #write in the html file
                #Make div
                f.write("<div>")
                #add image base, image corr
                f.write("<img src=\""+a[1]+"\" width=\"auto\" height=\"400\">&nbsp;<img src=\""+a[2]+"\" width=\"auto\" height=\"400\">")

                #add properties
                f.write("<br/><br/>")
                f.write("<img src=\""+b[1]+"\" width=\"auto\" height=\"400\">&nbsp;<img src=\""+b[2]+"\" width=\"auto\" height=\"400\">")
                #close div
                f.write("<br/><br/>")
                f.write("</div><p>human:"+str(a[0])+" auto:"+str(b[0])+"</p>")
                no+=1
f.close
print('\n true:'+str(ok));
print('false:'+str(no));
print('nc:'+str(nc));
