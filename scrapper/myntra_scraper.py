import time
from selenium.webdriver.common.by import By

from selenium import webdriver

def get_myntra_comments(url):
    driver = webdriver.Chrome()  # Or use another browser driver
    driver.get(url)
    time.sleep(5)
    for _ in range(4):  # Scroll 3 times to load more reviews
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new reviews to load
    reviews = driver.find_elements(By.CLASS_NAME, 'user-review-reviewTextWrapper')  # Replace with the correct class name
    review_texts = [review.text for review in reviews]
    driver.quit()
    return review_texts
