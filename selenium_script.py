from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time
import uuid
from datetime import datetime
import requests

# MongoDB setup
client = MongoClient("mongodb+srv://dhairyash:AuMuPu726@portfolio.mxcdeo3.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio")
db = client['twitter_trends']
collection = db['trending_topics']

# Twitter credentials
USERNAME = 'dheerizzler'
PASSWORD = 'DarTec@kh420'

# ProxyMesh setup
PROXY = 'http://dhairyash85:DarTec@kh420@us-ca.proxymesh.com:31280'

# Configure Selenium options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument(f"--proxy-server={PROXY}")

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open Twitter and login
    driver.get("https://x.com/i/flow/login")
    time.sleep(3)

    # Login flow
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(USERNAME)
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    # Navigate to homepage and fetch trends
    driver.get("https://x.com/home")
    time.sleep(5)

    trends = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")[:5]
    trending_topics = []
    for trend in trends:
        try:
            trend_text = trend.find_element(By.XPATH, ".//span").text
            trending_topics.append(trend_text)
        except:
            trending_topics.append("N/A")

    # Generate unique ID and collect metadata
    unique_id = str(uuid.uuid4())
    ip_address = requests.get("https://api.ipify.org").text  # Fetch current public IP
    timestamp = datetime.now()

    # Insert data into MongoDB
    data = {
        "unique_id": unique_id,
        "trend1": trending_topics[0] if len(trending_topics) > 0 else "N/A",
        "trend2": trending_topics[1] if len(trending_topics) > 1 else "N/A",
        "trend3": trending_topics[2] if len(trending_topics) > 2 else "N/A",
        "trend4": trending_topics[3] if len(trending_topics) > 3 else "N/A",
        "trend5": trending_topics[4] if len(trending_topics) > 4 else "N/A",
        "date_time": timestamp,
        "ip_address": ip_address
    }
    collection.insert_one(data)

    print("Data inserted into MongoDB successfully:")
    print(data)

finally:
    driver.quit()
