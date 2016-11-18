import json
from flask import Flask, render_template, request

#Config contains the AWS and Twitter Configuration details 
from config import AWS_ES_INDEX

#Settings authorizes the AWS credentials and connects to the ElasticSearch
from settings import es


application = Flask(__name__)

#Welcome.html is the HTML page which would be displayed first
@application.route('/')
def index():
	coords = []	#Stores the coordinates (Lattitude, Longitude) of the Tweets
	return render_template("welcome.html",
                           coords=json.dumps(coords),
                        )

#We get the category chosen by the user from the GET request
@application.route('/category', methods=['GET'])
def category():
	if request.method == 'GET':
		category = request.args.get('category') 
		#Retrieves the tweets related to the chosen category from the ElasticSearch
		es_data = es.search(index=AWS_ES_INDEX, body={"query": {"match": {"text": category}}}, size=600)
		coords = []
		for data in es_data['hits']['hits']:
			#If the tweet has a tagged location, then the geographical coordinates of the tweet are stored in Coords
			if len(data['_source']['coordinates']) > 0:
				geo_data = data['_source']['coordinates']['location'].split(',')
				lat = float(geo_data[0])
				lng = float(geo_data[1])
				coords.append([lat, lng])
		#Twittmap.html is the page where the heatmap would be rendered		
		return render_template("twittmap.html",
	                           coords=json.dumps(coords),
	                        )


if __name__ == "__main__":
    application.run(debug=True)
