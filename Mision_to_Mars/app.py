from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    # print(mars_data)
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():  
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_image()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_weather()
    mars_data = scrape_mars.scrape_hemispheres()

    mars_info.update({}, mars_data, upsert=True)
    

    return redirect("/", code=302)

   


if __name__ == "__main__":
    app.run(debug=True)


    