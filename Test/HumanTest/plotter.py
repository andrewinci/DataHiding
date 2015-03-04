import sqlite3
import matplotlib.pyplot as plt


tot = "select count(*) from comparated_image;"
sim = "select count(*) from comparated_image where is_similar = 1;"

db = sqlite3.connect("Link2.db")



sh = """select image1.url as 'Base', image2.url as 'Simi' ,comparated_image.SURF,comparated_image.correlation,comparated_image.is_similar from comparated_image
	inner join image as image1 on image1.id = comparated_image.img_base_id
	inner join image as image2 on image2.id = comparated_image.img_corr_id
	where comparated_image.img_base_path != comparated_image.img_corr_path
	and comparated_image.is_similar =1;"""

sh = db.execute(sh).fetchall()

st = ""
for x in sh:
	st += "<img src=\""+str(x[0])+"\" width=\"400\" height=\"400\">  - <img src=\""+x[1]+"\" width=\"400\" height=\"400\">  ::: "+ str(x[2]) + " -" + str(x[3]) + " <br/><br/> \n"

print
print st
print


kk = "select SURF,correlation,is_similar from comparated_image where img_base_path != img_corr_path;"

kk = db.execute(kk).fetchall()

xi = yi = xs = ys = []

for x in kk:
	if x[2] == 0:
		xi = xi + [x[0]]
		yi = yi + [x[1]]
	else:
		xs = xs + [x[0]]
		ys = ys + [x[1]]

plt.xlabel('SURF')
plt.ylabel('Correlation')

plt.plot(xi, yi, marker='o', linestyle='None', color='b')
plt.plot(xs, ys, marker='o', linestyle='None', color='r')

plt.show()






db.close()