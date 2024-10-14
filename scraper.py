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
def scrapePage(place_id, passedDriver=None):
    url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    time0 = time.time()
    if passedDriver:
        driver = passedDriver
    else:
        service = Service('chromedriver.exe')  # Update the path
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Runs the browser in headless mode.
        options.add_argument('--lang=en-GB')
        driver = webdriver.Chrome(service=service, options=options)


    # Open Google Maps URL (sample business)

    # <button class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc" jscontroller="soHxf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" data-idom-class="nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc" jsname="tWT92d" aria-label="Reject all"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-J1Ukfc-LhBDec"></div><div class="VfPpkd-RLmnJb"></div><span jsname="V67aGc" class="VfPpkd-vQzf8d">Reject all</span></button>

    driver.get(url) # "https://www.google.com/maps/place/East-West+Pub/@60.1990582,24.9378081,17z/data=!4m8!3m7!1s0x469209901ebb1ad3:0xd6ab54bd134e1f1f!8m2!3d60.1990582!4d24.940383!9m1!1b1!16s%2Fg%2F11ckkyrnfx?entry=ttu&g_ep=EgoyMDI0MDkyNS4wIKXMDSoASAFQAw%3D%3D"
    
    
    # Wait for the reviews to load
    time.sleep(2)
    try:
        reviews = driver.find_element(By.XPATH, "//button//div//div[contains(text(), 'Reviews')]")
    except:
    #    print(f'Error {e}')
       return []
    reviews.click()
    time.sleep(1)
    actions = ActionChains(driver)
    element = driver.find_element(By.CLASS_NAME, 'fontDisplayLarge') # wiI7pd
    try:
        element.click()
    except e:
        print(f'Error: {e}')
        return []
    for _ in range(50):  # Adjust range as necessary to load more reviews
        # print('scroll')
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.2)
    # time.sleep(200)
    
    # Extract page source and pass it to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the review elements (the exact tag/class might change)
    reviews = soup.find_all('div', class_='jftiEf fontBodyMedium')  # Update class as per actual HTML

    # Parse the reviews
    reviewtexts = []
    for review in reviews:
        # Find review text
        try:
          span = review.find('span', class_='wiI7pd')
          if span:
            review_text = span.text
            reviewtexts.append(review_text)
        except e:
          print(f'error {e}')
          continue
        # print("Review:", review_text)

        # Find the rating
        # rating = review.find('span', class_='kvMYJc').text
        # print("Rating:", rating)
        # print("\n")
    
    # Close the browser
    # driver.quit()
    print('reviews scraped:', len(reviewtexts))
    print('time elapsed:', time.time() - time0)
    return reviewtexts

if __name__ == '__main__':
    scrapePage("ChIJV04qDAAJkkYRwltKh2f6YJ8")