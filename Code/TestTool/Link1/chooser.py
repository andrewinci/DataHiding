#!/usr/local/bin/python3
import sqlite3

def computesimilarity():

    sh = db.execute("""select
    image_base.url,
    image_corr.url,
    comparated_image.SURF as 'S',
    comparated_image.correlation as 'corr',
    comparated_image.is_similar as 'is_sim',
    comparated_image.arg2,
    comparated_image.img_base_id,
    comparated_image.img_corr_id
    from comparated_image
    inner join image as image_base on image_base.id = comparated_image.img_base_id
    inner join image as image_corr on image_corr.id = comparated_image.img_corr_id
    order by S""").fetchall()

    sh = db.execute('select SURF,correlation,is_similar, arg2 from comparated_image').fetchall();

    for x in sh:
        #variable result from query
        minSurf = x[1]
        correlation = x[2]
        is_sim=str(x[3])
        maxSurf = x[4]

        if is_sim=='2':
            #no face in both image
            if(correlation>1/2 and maxSurf+minSurf>0.35):
                is_sim ='1'
            if(pow(correlation,2)>1/2):
                is_sim ='1'
            if(maxSurf + minSurf > 0.4):
                is_sim ='1'
        elif is_sim == '1':
            #common face
            sim="yes"
        else:
            #no common face
            is_sim ='0'
        if is_sim == '2':
            is_sim='0'

        #update database
        db.execute('update comparated_image set is_similar = ? where img_base_id = ? and img_corr_id = ?',[str(is_sim),img_base_id, img_corr_id])
    db.commit()
    db.close()

def printresult(db):

    sh = db.execute("""select
    image_base.url,
    image_corr.url,
    comparated_image.SURF as 'S',
    comparated_image.correlation as 'corr',
    comparated_image.is_similar as 'is_sim',
    comparated_image.arg2,
    comparated_image.img_base_id,
    comparated_image.img_corr_id
    from comparated_image
    inner join image as image_base on image_base.id = comparated_image.img_base_id
    inner join image as image_corr on image_corr.id = comparated_image.img_corr_id
    order by S""").fetchall()

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
        #variable result from query
        minSurf = x[2]
        correlation = x[3]
        is_sim=str(x[4])
        maxSurf = x[5]
        info = 'none'
        img_base_id = x[6]
        img_corr_id = x[7]

        #TODO: remove if all work
        if is_sim=='2':
            #no face in both image
            sim="nc"
            if(correlation>1/2 and maxSurf+minSurf>0.35):
                sim ="yes"
                info = "correlation>1/2 and maxSurf+minSurf"
                is_sim ='1'
            if(pow(correlation,2)>1/2):
                sim ="yes"
                info = "correlation"
                is_sim ='1'
            if(maxSurf + minSurf > 0.4):
                sim = "yes"
                info = "max and min SURF"
                is_sim ='1'
        elif is_sim == '1':
            #common face
            sim="yes"
            info = "face detection"
        else:
            #no common face
            is_sim ='0'
            sim="no"
            info = "face detection"

        if is_sim == '2':
            is_sim='0'

        #Web page for show the result
        #Make div
        f.write("<div class="+sim+">")
        #add image base, image corr
        f.write("<img src=\""+x[0]+"\" width=\"auto\" height=\"400\">&nbsp;<img src=\""+x[1]+"\" width=\"auto\" height=\"400\">")
        #add properties
        f.write("<h1>"+sim+"</h1><h2> minSURF:"+ str(minSurf) + " Correlation:" + str(correlation) +" IsSimilar:"+is_sim+" Arg2:"+str(maxSurf)+" info:"+info +"</H2> <br/><br/>")
        #close div
        f.write("</div>")
        #update database
        db.execute('update comparated_image set is_similar = ? where img_base_id = ? and img_corr_id = ?',[str(is_sim),img_base_id, img_corr_id])
    f.close()
    db.commit()
    db.close()
    from subprocess import call
    call(["open", "view.html"]);


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("db", help="database with image and articles")
    args = parser.parse_args()
    db_path = args.db
    db = sqlite3.connect(db_path)
    printresult(db)
