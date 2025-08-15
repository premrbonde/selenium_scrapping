import time
import os
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INSTAGRAM_USERNAME = os.getenv("IG_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("IG_PASSWORD")
NUM_POSTS = int(os.getenv("NUM_POSTS", 10))  # default to 10 if not set


def scrape_instagram_posts():
    scraped_data = []

    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.instagram.com/")
    time.sleep(5)
    wait = WebDriverWait(driver, 15)

    # Step 1: Login
    driver.find_element(By.NAME, "username").send_keys(INSTAGRAM_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(INSTAGRAM_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(10)

    # Step 2: Search for profile
    search_icon = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Search' and contains(@class, 'x1lliihq')]")
    ))
    search_icon.click()

    search_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@aria-label='Search input']")
    ))
    search_box.send_keys("burgerkingindia")
    time.sleep(1)

    burgerking_span = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//span[normalize-space()='burgerkingindia']"
    )))
    burgerking_span.click()

    # Step 3: Open first post
    first_post_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//article//a"))
    )
    driver.execute_script("arguments[0].click();", first_post_link)

    # Step 4: Scrape posts
    for i in range(NUM_POSTS):
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Likes
        likes_outer = soup.find(
            "span",
            class_="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi xpm28yp x8viiok x1o7cslx"
        )
        likes_inner = likes_outer.find("span", class_="html-span") if likes_outer else None
        likes_count = likes_inner.get_text(strip=True) if likes_inner else None

        # Description
        description_tag = soup.select_one("div._a9zr h1._ap3a._aaco._aacu._aacx._aad7._aade")
        description = description_tag.get_text(" ", strip=True) if description_tag else None

        # First comment
        comment_container = soup.select_one("div._a9zr div.xt0psk2 span._ap3a._aaco._aacu._aacx._aad7._aade")
        first_comment = comment_container.get_text(strip=True) if comment_container else None

        # Hashtags
        hashtags = [a.get_text(strip=True) for a in soup.select("a[href*='/explore/tags/']")]
        hashtags_text = ", ".join(hashtags)

        scraped_data.append({
            "Likes": likes_count,
            "Description": description,
            "First_Comment": first_comment,
            "Hashtags": hashtags_text,
            "Post_Number": i + 1
        })

        print(f"Scraped post {i + 1}")

        # Next button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh button._abl-")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
        except Exception:
            print("No more posts found.")
            break

    driver.quit()
    return scraped_data


if __name__ == "__main__":
    data = scrape_instagram_posts()
    print(f"Total posts scraped: {len(data)}")
