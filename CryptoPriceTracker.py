# Cryptocurrency Price Tracker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

print(" Starting Cryptocurrency Price Tracker...")

# Chrome setup
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Launch Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open CoinMarketCap website
url = "https://coinmarketcap.com/"
driver.get(url)
time.sleep(5)

# Get the top 10 cryptocurrency details
rows = driver.find_elements(By.XPATH, "//tbody/tr")[:10]

data = []
for row in rows:
    try:
        name = row.find_element(By.XPATH, ".//td[3]//p").text
        price = row.find_element(By.XPATH, ".//td[4]//span").text
        change_24h = row.find_element(By.XPATH, ".//td[5]//span").text
        market_cap = row.find_element(By.XPATH, ".//td[8]//p").text

        data.append({
            "Name": name,
            "Price": price,
            "24h Change": change_24h,
            "Market Cap": market_cap,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        print(" Skipped a row due to:", e)

# Save data into a CSV file
if data:
    df = pd.DataFrame(data)
    df.to_csv("crypto_prices.csv", index=False)
    print("Data saved successfully as crypto_prices.csv")
else:
    print(" No data found!")

driver.quit()
print(" Done!")