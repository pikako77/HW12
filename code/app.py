from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_db = mongo.db.scrape_dict.find_one()
    return render_template("index.html", mars_db=mars_db)


@app.route("/scrape")
def scrape():
    mars_db = mongo.db.scrape_dict
    scrape_dict_data = scrape_mars.scrape_all()
    mars_db.update({}, scrape_dict_data, upsert=True)
    return ("done")


if __name__ == "__main__":
    app.run(debug=True, port=50001)