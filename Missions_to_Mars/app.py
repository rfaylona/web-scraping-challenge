from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def home():

    latest_mars_data = mongo.db.collection.find_one()
    return render_template("index.html", data=latest_mars_data)

@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()
    mongo.db.collection.update_many({}, {"$set": mars_data}, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)