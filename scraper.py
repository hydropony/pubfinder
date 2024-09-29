from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Initialize the Chrome browser with Selenium
service = Service('./chromedriver')  # Update the path
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Runs the browser in headless mode.
driver = webdriver.Chrome(service=service, options=options)

# Open Google Maps URL (sample business)

# <button class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc" jscontroller="soHxf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" data-idom-class="nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc" jsname="tWT92d" aria-label="Reject all"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-J1Ukfc-LhBDec"></div><div class="VfPpkd-RLmnJb"></div><span jsname="V67aGc" class="VfPpkd-vQzf8d">Reject all</span></button>

driver.get("https://www.google.com/maps/place/East-West+Pub/@60.1990582,24.9378081,17z/data=!4m8!3m7!1s0x469209901ebb1ad3:0xd6ab54bd134e1f1f!8m2!3d60.1990582!4d24.940383!9m1!1b1!16s%2Fg%2F11ckkyrnfx?entry=ttu&g_ep=EgoyMDI0MDkyNS4wIKXMDSoASAFQAw%3D%3D")

# Wait for the "Accept all" button to appear (you might need to adjust this depending on Google's structure)
try:
    # Wait until the cookies consent "Accept all" button is present and clickable
    reject_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(), 'Accept all')]"))
    )
    reject_button.click()  # Click the "Accept all" button

    print("Cookies consent rejected.")

except Exception as e:
    print("Error clicking the cookies button:", e)
  
# Wait for the reviews to load
time.sleep(5)

# body = driver.find_element(By.CLASS_NAME, "iwhWtc") # e07Vkf kA9KIf
element = driver.find_element(By.CLASS_NAME, 'kA9KIf')
actions = ActionChains(driver)

# Move the cursor to the element
# print(element.location)
# actions.move_to_element(element).click().perform()
time.sleep(2)
element.send_keys(Keys.DOWN)
time.sleep(2)
# body = driver.find_element(By.TAG_NAME, "body")
# body.send_keys(Keys.TAB)
# time.sleep(2)
# body = driver.find_element(By.TAG_NAME, "body")
# body.send_keys(Keys.TAB)
# time.sleep(2)
# body.send_keys(Keys.TAB)
# time.sleep(2)
# Scroll down to load all reviews (scrolling multiple times to load more)
for i in range(10):  # Adjust range as necessary to load more reviews
    print('scroll')
    driver.execute_script("window.scrollBy(0, 1000);")
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)

# Extract page source and pass it to BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all the review elements (the exact tag/class might change)
reviews = soup.find_all('div', class_='jftiEf fontBodyMedium')  # Update class as per actual HTML

# Parse the reviews
for review in reviews:
    # Find review text
    try:
      review_text = review.find('span', class_='wiI7pd').text
    except e:
      print(f'error {e}')
      continue
    print("Review:", review_text)

    # Find the rating
    rating = review.find('span', class_='kvMYJc').text
    print("Rating:", rating)
    print("\n")

# Close the browser
driver.quit()
