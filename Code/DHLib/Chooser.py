#!/usr/local/bin/python3n
import sqlite3

def computesimilarity(db):
    sh = db.execute('select SURFmin , SURFmax, correlation, is_similar, img_base_id, img_corr_id from comparated_image').fetchall();
    for x in sh:
        #variable result from query
        minSurf = x[0]
        maxSurf = x[1]
        correlation = x[2]
        is_sim = str(x[3])
        img_base_id = x[4]
        img_corr_id = x[5]
        if is_sim=='2':
            #no face in both image
            if(correlation>1/2 and maxSurf+minSurf>0.35):
                info = "correlation>1/2 and maxSurf+minSurf"
                is_sim ='1'
            if(pow(correlation,2)>1/2):
                info = "correlation"
                is_sim ='1'
            if(maxSurf + minSurf > 0.4):
                info = "max and min SURF"
                is_sim ='1'
        elif is_sim == '1':
            #common face
            info = "face detection"
        else:
            #no common face
            is_sim ='0'
            info = "face detection"
        if is_sim == '2':
            is_sim='0'
            info = 'not sure'
            if( maxSurf>0 and minSurf>0 and correlation+maxSurf+minSurf>0.5):
                is_sim='1'
                info = 'c+Ms+ms>0.5'

        #update database
        db.execute('''update comparated_image set is_similar = ?, info = ?
        where img_base_id = ? and img_corr_id = ?''',
        [str(is_sim), info, img_base_id, img_corr_id])
    db.commit()

if __name__ == '__main__':
    db = sqlite3.connect('../cache/articles.db')
    computesimilarity(db)
