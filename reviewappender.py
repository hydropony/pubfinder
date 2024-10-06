from scraper import scrapePage
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

places = pd.read_json('Helsinki_pubs_reviews.json')

service = Service('chromedriver.exe')  # Update the path
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Runs the browser in headless mode.
options.add_argument('--lang=en-GB')
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com/maps/place/?q=place_id:ChIJV04qDAAJkkYRwltKh2f6YJ8") 

# Wait for the "Accept all" button to appear (you might need to adjust this depending on Google's structure)
time.sleep(1)
try:
    # Wait until the cookies consent "Accept all" button is present and clickable
    reject_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(), 'Accept all')]"))
    )
    reject_button.click()  # Click the "Accept all" button

    # print("Cookies consent rejected.")

except Exception as e:
    print("Error clicking the cookies button:", e)


start_index = 297
time0 = time.time()
for index, row in places.iterrows():
    if index < start_index:
        continue

    place_url = row['place_id']
    print(f"scraping place {row['name']}")
    reviews = scrapePage(place_url, driver) # doesn't work with driver passed :(
    
    # Add reviews as a new column to the DataFrame
    # print(np.array(reviews))

    places.at[index, 'reviews'] = np.array(reviews)
    places.to_json('Helsinki_pubs_reviews.json')
    # i += 1

# Display updated DataFrame
print(places)
places.to_json('Helsinki_pubs_reviews.json')
print(f'Elapsed time: {time.time() - time0}')