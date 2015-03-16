import sqlite3
import datetime
import sys


def timeToString(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y,%m,%d')

def queryDB(db,query):
	return sqlite3.connect(db).execute(query).fetchall()

def saveJSONP(dataBase, newsBase, newsCorr):
    out_file = open("TimeVisualizator/time.jsonp","w")
    out_file.write("""
storyjs_jsonp_data = {
    "timeline":
    {
        "headline":"TimeVisualizator",
        "type":"default",
        "text":"<p>"""+ db +""" - """ + newsBase['title'] + """</p>",
        "date": [
            {
                "startDate":\""""+ newsBase['data'] +"""\",
                "endDate":\""""+ newsBase['data'] +"""\",
                "headline": "<b><a href='"""+ newsBase['url'] +"""' target='_blank'>""" + newsBase['title'] + """</a></b>",
                "text":" """+ ''.join(["<img src='"+i+"' height='300' width='300' /> <br/> <hr /><br/>" for i in newsBase['images']]) +""" "
            }""" + ''.join([""",{
                "startDate":\""""+ j['data'] +"""\",
                "endDate":\""""+ j['data'] +"""\",
                "headline": "<a href='"""+ j['url'] +"""' target='_blank'>""" + j['title'] + """</a>",
                "text":" """+ ''.join(["<img src='"+i[0]+"' height='250' width='250' /> <img src='"+i[1]+"' height='250' width='250' /> <br/><hr /><br/>" for i in j['images']]) +""" "
            }""" for j in newsCorr]) +"""
        ]
        
        ,
        "era": [
                {
                    "startDate":\""""+ newsBase['data'] +"""\",
                    "endDate":\""""+ newsBase['dataF'] +"""\",
                    "headline":"Original News"
                }

            ]
    }
}
        """)
    out_file.close()


def createFile(db):
    baseNewsQ = queryDB(db,"""
        select article.title , article.url, article.data , image.url from article
        inner join image
        on image.article_id = article.id
        where article.is_base = 1;
        """)
    try:
        baseNews = {
            'title' : baseNewsQ[0][0],
            'url' : baseNewsQ[0][1],
            'data' : timeToString(int(baseNewsQ[0][2])),
            'dataF' : timeToString(86400+ int(baseNewsQ[0][2])),
            'images' : [ i[3] for i in baseNewsQ]
        }
    except:
        print "There's no information about time."   
        sys.exit() 
    

    corrNewsQ = queryDB(db, """
        select temp2.title, temp2.url as "Surl", temp2.data as 'Sdata' , temp1.imageUrl as "Biurl", temp2.imageUrl as "Siurl" from comparated_image
        
        inner join
            (select article.id as 'id' , article.url as 'url', article.data as 'data' , image.id as 'imageid' , image.url as "imageUrl"
            from image
            inner join article on image.article_id = article.id
            where article.data is not null) as temp1
        on temp1.imageid = comparated_image.img_base_id

        inner join (select article.id as 'id' , article.title as 'title',  article.url as 'url', article.data as 'data' , image.id as 'imageid', image.url as "imageUrl"
            from image
            inner join article on image.article_id = article.id
            where article.data is not null) as temp2
        on temp2.imageid = comparated_image.img_corr_id

        where (comparated_image.is_similar == 1)
        and temp1.id <> temp2.id
        order by Surl;
    """)

    corrNews = []
    ind = list(set([corrNewsQ[i][1] for i in range(len(corrNewsQ))]))

    for i in ind:
        imge = []
        for j in corrNewsQ:
            if j[1] == i:
                imge += [(j[3],j[4])]
        corrNews += [{
            'title' : j[0],
            'url' : j[1],
            'data' : timeToString(int(j[2])),
            'images' : imge
        }]
        
    saveJSONP(db,baseNews,corrNews)


db = "articles.db"
createFile(db)