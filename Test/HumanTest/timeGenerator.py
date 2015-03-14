import sqlite3

def queryDB(db,query):
	return sqlite3.connect(db).execute(query).fetchall()

def saveHTML(dataBase , dateCorr, dbName):

	dran = [min(dateCorr + [dataBase]), max(dateCorr+ [dataBase])]

	dateC = (''.join([ " new Date("+str(i)+") ,"  for i in dateCorr ]))[0:-1]

	out_file = open("TimeVisualizator/time.html","w")

	g = """
<!DOCTYPE html>
<meta charset="utf-8">
<html>
    <head>
        <link rel="stylesheet" href="style.css" />
        <style type="text/css">
        body {
            font-family: verdana, sans-serif;
        }
        </style>
    </head>
    <body>
        <div style="text-align: center">
            <h1>TimeVisualizator - """ + dbName + """</h1>
        

        <div id="chart_placeholder"></div>
        <br/>
        <div id="legend"></div>
    </div>    
        <br />
        """ + """<script src="d3.js"></script>
        <script src="eventDrops.js"></script>
        
        <script>
            var chartPlaceholder = document.getElementById('chart_placeholder');
            var names = ["Original News", "Correlated News"];

            var data = [
			  { name: "Base News", dates: [new Date("""+ str(dataBase) +""")]},
			  { name: "Corr News", dates: ["""+ dateC +"""] }
			];

            
            var color = d3.scale.category20();

            var locale = d3.locale({
                "decimal": ",",
                "thousands": " ",
                "grouping": [3],
                "dateTime": "%A %e %B %Y, %X",
                "date": "%d/%m/%Y",
                "time": "%H:%M:%S",
                "periods": ["AM", "PM"],
                "days": ["domenica", "lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato"],
                "shortDays": ["D", "L", "M", "Me", "G", "V", "S"],
                "months": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
                "shortMonths": ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
            });

            var graph = d3.chart.eventDrops()
            	.start(new Date(""" + str(dran[0] -100000000) + """))
                .end(new Date(""" + str(dran[1]   +100000000) + """))
                .minScale(0.5)
                .maxScale(100)
                .locale(locale)
                .eventColor(function (datum, index) {
                    if (datum.getTime() < """ + str(dataBase) + """) {
                        return 'red';
                    }
                    else if (datum.getTime() > """ + str(dataBase) + """){
                    	return 'orange';
                    }
                    return 'green';
                })
                .width(1000)
                .margin({ top: 100, left: 200, bottom: 0, right: 0 })
                .axisFormat(function(xAxis) {
                    xAxis.ticks(5);
                })
                .eventHover(function(el) {
                    var series = el.parentNode.firstChild.innerHTML;
                    var timestamp = d3.select(el).data();
                    document.getElementById('legend').innerHTML = '[' + timestamp + ']';
                })
                .eventZoom(function (scale) {
                    var limit = scale.domain();
                    var period = parseInt((limit[1] - limit[0]) / (60 * 60 * 1000) );
                })
                ;

            var element = d3.select(chartPlaceholder).append('div').datum(data);
            graph(element);

            var updateDelimiter = function (value) {
                graph.hasDelimiter(!graph.hasDelimiter())(element);
            };

        </script>

    </body>
</html>
	
	"""

	# <div id="content">
    # <div id="left">
    # </div>
    # </div>
        
	out_file.write(g)
	out_file.close()


def createFile(db):
	kk = queryDB(db, """
		select temp1.url as "Burl", temp2.url as "Surl",temp1.imageUrl as "Biurl", temp2.imageUrl as "Siurl", temp1.data as 'Bdata', temp2.data as 'Sdata' from comparated_image
		
		inner join
			(select article.url, article.data as 'data' , image.id as 'imageid' , image.url as "imageUrl"
			from image
			inner join article on image.article_id = article.id
			where article.data is not null) as temp1
		on temp1.imageid = comparated_image.img_base_id

		inner join (select article.url, article.data as 'data' , image.id as 'imageid', image.url as "imageUrl"
			from image
			inner join article on image.article_id = article.id
			where article.data is not null) as temp2
		on temp2.imageid = comparated_image.img_corr_id

		where comparated_image.img_base_path != comparated_image.img_corr_path
		and comparated_image.is_similar = 1
		and comparated_image.SURF < 1
		and Burl != Surl;
	""")
	if len(kk) != 0:
		data = int(kk[0][4])*1000
		dateC = [int(i[5])*1000 for i in kk ]

		saveHTML(data,dateC,db)
	else:
		print "No date to print"


db = "Link4.db"
createFile(db)