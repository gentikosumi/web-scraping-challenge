from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    facts = mongo.db.facts.find_one()
    # print(mars_data)
    return render_template("index.html", facts=facts)

@app.route("/scrape")
def scrape():  
    facts = mongo.db.data
    facts_data = scrape_mars.scrape()
    data.update({}, facts_data, upsert=True)
    

    return redirect("/", code=302)

   


if __name__ == "__main__":
    app.run(debug=True)


    