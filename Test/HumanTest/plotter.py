import sqlite3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

dbes = ["Link"+str(i+1)+".db" for i in range(4)]

xi = [[],[],[],[]]
yi = [[],[],[],[]]
xs = [[],[],[],[]]
ys = [[],[],[],[]]
zs = [[],[],[],[]]


for ilk in dbes:

	# print "\n Entering "+ ilk
	db = sqlite3.connect(ilk)


	tot = "select count(*) from comparated_image;"
	sim = "select count(*) from comparated_image where is_similar = 1;"

	

	tot = db.execute(tot).fetchall()
	sim = db.execute(sim).fetchall()

	# print " Tot : " + str(tot[0]) + " -  Sim : " + str(sim[0]) 

	# Commento

	# sh = db.execute("""
	# 	select image1.url as 'Base', image2.url as 'Simi' ,comparated_image.SURF,comparated_image.correlation,comparated_image.is_similar from comparated_image
	# 	inner join image as image1 on image1.id = comparated_image.img_base_id
	# 	inner join image as image2 on image2.id = comparated_image.img_corr_id
	# 	where comparated_image.img_base_path != comparated_image.img_corr_path
	# 	and comparated_image.is_similar =1;"""
	# 	).fetchall()

	# print '\n'.join(["<img src=\""+x[0]+"\" width=\"400\" height=\"400\">  - <img src=\""+x[1]+"\" width=\"400\" height=\"400\">  ::: "+ str(x[2]) + " -" + str(x[3]) + " <br/><br/> " for x in sh])



	# kk = "select SURF,correlation,is_similar from comparated_image where img_base_path != img_corr_path;"

	ij = db.execute("""
		select SURF,correlation,is_similar
		from comparated_image
		where img_base_path != img_corr_path
		and SURF<1
		;"""
		).fetchall()

	kk = db.execute("""
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
	where comparated_image.img_base_path != comparated_image.img_corr_path;
	""").fetchall()

	# and (Bdata != '' or Sdata != '');

	# ij = kk


	# kk = db.execute("""
	# 	select image1.url as 'Base', image2.url as 'Simi' ,comparated_image.SURF,comparated_image.correlation,comparated_image.is_similar from comparated_image
	# 	inner join image as image1 on image1.id = comparated_image.img_base_id
	# 	inner join image as image2 on image2.id = comparated_image.img_corr_id
	# 	where comparated_image.img_base_path != comparated_image.img_corr_path
	# 	and comparated_image.is_similar =1;"""
	# 	).fetchall()


	# Variabili da plottare

	# SURFCORR Time
	for x in kk:
		if x[2] == 0:
			xi[dbes.index(ilk)] += [x[3]]
			yi[dbes.index(ilk)] += [x[4]]
		else:
			xs[dbes.index(ilk)] += [x[3]]
			ys[dbes.index(ilk)] += [x[4]]
			zs[dbes.index(ilk)] += [(x[1] - x[0])/10000]
	
	for x in ij:
		if x[2] == 0:
			xi[dbes.index(ilk)] += [x[0]]
			yi[dbes.index(ilk)] += [x[1]]
		else:
			xs[dbes.index(ilk)] += [x[0]]
			ys[dbes.index(ilk)] += [x[1]]
			

	# xi = [ x[2]==0 and x[0]  for x in ij]
	# yi = [ x[2]==0 and x[1]  for x in ij]
	# xs = [ x[2]==1 and x[0]  for x in ij]
	# ys = [ x[2]==1 and x[1]  for x in ij]


	# Plotting
	# print xi




	# plt.xlabel('Base Date')
	# plt.ylabel('Correlated Date')

	# x = np.linspace(140000, 150000, 10000)
	# y = np.linspace(140000, 150000, 10000)
	# # plt.axis([140000,150000,140000,150000])
	# plt.plot(x, y, 'r')

	# # plt.xlabel('SURF')
	# # plt.ylabel('Correlation')
	# # plt.axis([-0.05,1.05,-1.05,1.05])


	# plt.plot(xi[dbes.index(ilk)], yi[dbes.index(ilk)], marker='o', linestyle='None', color='b')
	# plt.plot(xs[dbes.index(ilk)], ys[dbes.index(ilk)], marker='o', linestyle='None', color='r')
	# plt.show()



	# Time 3d lul



	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection='3d')
	
	# # print str(len(xs[dbes.index(ilk)])) + " - " + str(len(ys[dbes.index(ilk)])) + " - " + str(len(zs[dbes.index(ilk)]))

	# ax.scatter(xs[dbes.index(ilk)], ys[dbes.index(ilk)],zs[dbes.index(ilk)]  , color='r', marker='o')

	# ax.set_xlabel('SURF')
	# ax.set_ylabel('Correlation')
	# ax.set_zlabel('BaseDate - CorrDate')

	# plt.show()

	db.close()

print "All together!"

plt.xlabel('SURF')
plt.ylabel('Correlation')
plt.axis([-0.05,1.05,-1.05,1.05])

# plt.xlabel('Base Date')
# plt.ylabel('Correlated Date')
# x = np.linspace(142000, 142600, 10000)
# y = np.linspace(142000, 142600, 10000)
# plt.axis([142000,142600,142000,142600])
# plt.plot(x, y, 'r')

for ilk in dbes:
	plt.plot(xi[dbes.index(ilk)], yi[dbes.index(ilk)], marker='o', linestyle='None', color='b')
	plt.plot(xs[dbes.index(ilk)], ys[dbes.index(ilk)], marker='o', linestyle='None', color='r')
plt.show()



# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# x = np.arange(-1, 1, 0.1)
# y = np.arange(-0.1, 1.1, 0.1)
# x_s,y_s = np.meshgrid(x, y)
# # print str(len(xs[dbes.index(ilk)])) + " - " + str(len(ys[dbes.index(ilk)])) + " - " + str(len(zs[dbes.index(ilk)]))
# for ilk in dbes:
# 	ax.scatter(xs[dbes.index(ilk)], ys[dbes.index(ilk)],zs[dbes.index(ilk)]  , color='r', marker='o')

# ax.plot_surface(x_s, y_s, 0 ,alpha=0.7)
# ax.set_xlabel('SURF')
# ax.set_ylabel('Correlation')
# ax.set_zlabel('BaseDate - CorrDate')

# plt.show()