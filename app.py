from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.mars_db

db.mars_collection.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    #mongo.mars_db.collection.update({}, mars, upsert=True)
    db.mars_collection.insert(mars)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)