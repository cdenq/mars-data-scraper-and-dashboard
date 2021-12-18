# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Scrape Route
@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape()
    listings.replace_one({}, listings_data, upsert = True)
    return redirect("/data")

# Display Data Route
@app.route("/data")
def data():
    mars_info = mongo.db.listings.find_one()
    return render_template("data.html", info = mars_info)

if __name__ == "__main__":
    app.run(debug=True)