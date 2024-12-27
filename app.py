from flask import Flask, jsonify
import subprocess
from pymongo import MongoClient
from flask_cors import CORS
# from CORS import cors
app = Flask(__name__)
CORS(app)
# MongoDB setup
client = MongoClient("mongodb+srv://dhairyash:AuMuPu726@portfolio.mxcdeo3.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio")
db = client['twitter_trends']
collection = db['trending_topics']

@app.route('/run-selenium', methods=['POST'])
def run_selenium():
    # Run the Selenium script
    subprocess.run(["python", "selenium_script.py"])
    
    # Fetch the latest data from MongoDB
    latest_entry = collection.find_one(sort=[("_id", -1)])
    return jsonify({
        "unique_id": latest_entry["unique_id"],
        "trend1": latest_entry["trend1"],
        "trend2": latest_entry["trend2"],
        "trend3": latest_entry["trend3"],
        "trend4": latest_entry["trend4"],
        "trend5": latest_entry["trend5"],
        "date_time": str(latest_entry["date_time"]),
        "ip_address": latest_entry["ip_address"]
    })

if __name__ == "__main__":
    app.run(debug=True)
