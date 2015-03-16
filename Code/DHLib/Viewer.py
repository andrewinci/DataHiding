#!/usr/local/bin/python3
import sqlite3

def printresult(db):

    sh = db.execute("""select
    image_base.url,
    image_corr.url,
    comparated_image.SURFmin as 'S',
    comparated_image.SURFmax,
    comparated_image.correlation as 'corr',
    comparated_image.is_similar as 'is_sim',
    comparated_image.info
    from comparated_image
    inner join image as image_base on image_base.id = comparated_image.img_base_id
    inner join image as image_corr on image_corr.id = comparated_image.img_corr_id
    order by is_sim""").fetchall()

    #Web page for show the result
    f = open('view.html','w')
    #add style
    f.write("""<head><style>h1 {
    color:red;
    font-family:courier;
    font-size:200%;
    }
    h2 {
    color:blue;
    font-family:courier;
    font-size:100%;
    }
    .yes {
    text-align: center;
    background:rgba(46, 255, 5, 0.23);
    }

    .no {
    text-align: center;
    background:rgba(147, 3, 14, 0.34);
    }

    .nc {
    text-align: center;
    background:rgba(255, 250, 46, 0.76);
    }
    </style></head>""")

    for x in sh:
        imgbaseurl = x[0]
        imgcorrurl = x[1]
        surfmin = x[2]
        surfmax = x[3]
        correlation = x[4]
        is_sim = x[5]
        info = x[6]
        if is_sim == 1:
             sim = 'yes'
        else:
            sim = 'no'
        #Make div
        f.write("<div class="+sim+">")
        #add image base, image corr
        f.write("<img src=\""+imgbaseurl+"\" width=\"auto\" height=\"400\">&nbsp;"+
                "<img src=\""+imgcorrurl+"\" width=\"auto\" height=\"400\">")
        #add properties
        f.write("<h1>"+sim+"</h1><h2> minSURF:"+ str(surfmin) +
                " Correlation:" + str(correlation) +" IsSimilar:"+str(is_sim)+
                " maxSURF:"+str(surfmax)+" info:"+info +"</H2> <br/><br/>")
        #close div
        f.write("</div>")
    f.close()
    from subprocess import call
    call(["open", "view.html"]);


if __name__ == '__main__':
    import sqlite3
    db = sqlite3.connect('../cache/articles.db')
    printresult(db)
