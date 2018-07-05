#coding:utf-8
import os,sys
from flask import Flask
from flask import request,url_for
from flask import render_template
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
import pyspark.mllib.recommendation as rd

global tmp,user
tmp = []
user = 0
app = Flask(__name__)
os.environ['JAVA_HOME']="/usr/lib/jvm/java-8-oracle/"
sys.path.append("/usr/lib/jvm/java-8-oracle/bin/")
sc = SparkContext()

@app.route('/', methods=['GET', 'POST'])
def index():
	u = request.values.get("u")
	if request.method == 'POST':
		f = open("./ex.txt","r")
		s= f.read()
		if(s.find(str(u))!= -1):
			f = open("./u.data","r")
			rawData = sc.textFile("./u.data")
			moive = sc.textFile("./u.item")
			rawRatings = rawData.map(lambda line : line.split("\t")[:3])
			ratings = rawRatings.map(lambda line : rd.Rating(int(line[0]),int(line[1]),float(line[2])))
			model = rd.ALS.train(ratings,50,5,0.01)
			products = model.recommendProducts(int(u),10)
			title_data = moive.map(lambda line:line.split("|")[:2]).collect()
			titles = dict(title_data)
			moivesForUser = ratings.keyBy(lambda rating:rating.user).lookup(int(u))
			moivesForUser = sorted(moivesForUser,key = lambda r: r.rating,reverse=True)[0:10]
			s=[(titles[str(r.product)], r.rating) for r in products]
			return render_template("main.html",**locals())
		else:
			return render_template("error.html")	
	return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)