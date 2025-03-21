import time
import random
from selenium.webdriver.common.by import By
from utils import init_driver

def get_amazon_comments(url, max_reviews=50):
    driver = init_driver()
    driver.get(url)
    time.sleep(5)

    comments = []
    while len(comments) < max_reviews:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))

        reviews = driver.find_elements(By.CSS_SELECTOR, 'span[data-hook="review-body"]')
        for review in reviews:
            comment = review.text.strip()
            if comment and comment not in comments:
                comments.append(comment)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(random.uniform(4, 6))
        except:
            break

    driver.quit()
    return comments[:max_reviews]
