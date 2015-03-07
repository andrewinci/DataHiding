import sqlite3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import re


def justName(st):
	return re.match(r"([\w]*)(?:.)" , st).group()


# For Plot I intend "Save In A File"


# Search on db a given query
# No try catch. Please give correct name and query

def queryDB(db,query):
	return sqlite3.connect(db).execute(query).fetchall()


# Query and plot comparated Images
# Just give the correct db name

def qpComparated(db,draw = True):
	ij = queryDB(db , """
	select SURF,correlation,is_similar
	from comparated_image
	where img_base_path != img_corr_path
	and SURF<1
	;""")
	
	# Gen variables for plotting

	xi = []
	xs = []
	yi = []
	ys = []

	for x in ij:
		if x[2] == 0:
			xi += [x[0]]
			yi += [x[1]]
		else:
			xs += [x[0]]
			ys += [x[1]]

	# Plotting

	plt.xlabel('SURF')
	plt.ylabel('Correlation')
	plt.axis([-0.05,1.05,-1.05,1.05])

	plt.plot(xi, yi, marker='o', linestyle='None', color='b')
	plt.plot(xs, ys, marker='o', linestyle='None', color='r')
	
	plt.savefig(justName(db)+'Compared.png', bbox_inches='tight',format="png")
	if (draw) : plt.show()

	return xi,yi,xs,ys




# Query and plot comparated Images over time
# Just give the correct db name

def qpTimeCompare(db , draw = True):
	kk = queryDB(db, """
		select temp1.data as 'Bdata', temp2.data as 'Sdata', comparated_image.is_similar, comparated_image.SURF , comparated_image.correlation from comparated_image
		inner join (select article.data as 'data' , image.id as 'imageid'
		from image
		inner join article on image.article_id = article.id
		where article.data is not null) as temp1
		on temp1.imageid = comparated_image.img_base_id
		inner join (select article.data as 'data' , image.id as 'imageid'
		from image
		inner join article on image.article_id = article.id
		where article.data is not null) as temp2
		on temp2.imageid = comparated_image.img_corr_id
		where comparated_image.img_base_path != comparated_image.img_corr_path
		and comparated_image.SURF < 1;
	""")


	xi = []
	xs = []
	yi = []
	ys = []
	zs = []


	# SURFCORR Time
	for x in kk:
		if x[2] == 0:
			xi += [x[3]]
			yi += [x[4]]
		else:
			xs += [x[3]]
			ys += [x[4]]
			zs += [(x[1] - x[0])/10000]


	# Plotting in 3d

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	x = np.arange(-0.1, 1.1, 0.1)
	y = np.arange(-1.1, 1.1, 0.1)
	x_s,y_s = np.meshgrid(x, y)

	ax.scatter(xs, ys ,zs  , color='r', marker='o')

	ax.plot_surface(x_s, y_s, 0 ,alpha=0.7)
	ax.set_xlabel('SURF')
	ax.set_ylabel('Correlation')
	ax.set_zlabel('BaseDate - CorrDate')
	
	plt.savefig(justName(db)+'TimeComp.png', bbox_inches='tight',format="png")
	if (draw) : plt.show()

	return xs,ys,zs


# Query plot from a list of dbes the complete scenario

def qpComparatedAll(dbes, draw=True):
	xi = [[] for i in range(len(dbes))]
	yi = [[] for i in range(len(dbes))]
	xs = [[] for i in range(len(dbes))]
	ys = [[] for i in range(len(dbes))]
	zs = [[] for i in range(len(dbes))]

	# Plot Compared graph

	for db in dbes:
		print "Compared "+ db
		xi[dbes.index(db)] , yi[dbes.index(db)] , xs[dbes.index(db)] , ys[dbes.index(db)] = qpComparated(db,draw=draw)

	# Plotting

	plt.xlabel('SURF')
	plt.ylabel('Correlation')
	plt.axis([-0.05,1.05,-1.05,1.05])

	for db in dbes:
		plt.plot(xi[dbes.index(db)], yi[dbes.index(db)], marker='o', linestyle='None', color='b')
		plt.plot(xs[dbes.index(db)], ys[dbes.index(db)], marker='o', linestyle='None', color='r')

	plt.savefig('ComparedAll.png', bbox_inches='tight',format="png")
	if (draw) : plt.show()

	# Plot Time graph

	for db in dbes:
		print "Compared "+ db
		xs[dbes.index(db)] , ys[dbes.index(db)] , zs[dbes.index(db)]  = qpTimeCompare(db,draw=draw)

	# Plotting in 3d

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')


	x = np.arange(-0.1, 1.1, 0.1)
	y = np.arange(-1.1, 1.1, 0.1)
	x_s,y_s = np.meshgrid(x, y)

	for db in dbes:
		ax.scatter(xs[dbes.index(db)] , ys[dbes.index(db)] , zs[dbes.index(db)]  , color='r', marker='o')

	ax.plot_surface(x_s, y_s, 0 ,alpha=0.7)
	ax.set_xlabel('SURF')
	ax.set_ylabel('Correlation')
	ax.set_zlabel('BaseDate - CorrDate')

	plt.savefig('TimeCompAll.png', bbox_inches='tight',format="png")
	if (draw) : plt.show()


# All you need is the list of dbes
dbes = ["Link"+str(i+1)+".db" for i in range(4)]

qpComparatedAll(dbes)
