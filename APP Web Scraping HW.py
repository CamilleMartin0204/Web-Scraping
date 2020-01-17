#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template
from flask import jsonify
from scrape_mars import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.team_db

# Set route
@app.route('/')
def index():
    # Store the entire marsData collection in a list
    marsDb = list(db.marsData.find())
    print(marsDb)

    # Return the template with the marsDb list passed in
    return render_template('index.html', marsDb=marsDb)

@app.route("/scrape", methods=['GET'])
def scapeRoute():
    scrapeResults = scrape()
    jsondResults = jsonify(scrapeResults)

    # Drops collection if available to remove duplicates
    db.marsData.drop()

    # Creates a collection in the database and inserts two documents
    db.marsData.insert_many([scrapeResults])

    return jsondResults


if __name__ == "__main__":
    app.run(debug=True)

