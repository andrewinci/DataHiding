import sqlite3

def queryDB(db,query):
	return sqlite3.connect(db).execute(query).fetchall()


dbes = ["Charlie.db","Cyclone.db","ISIS.db","TurkishAirlines.db","Russia.db"]

for i in dbes:
	count = queryDB(i,"select count(*) from comparated_image;")[0][0]
	simcount = queryDB(i,"select count(*) from comparated_image where is_similar = 1;")[0][0]
	print i + " - " + str(count) + " - " + str(simcount) 