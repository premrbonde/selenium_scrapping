import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def scrape_burgerking_products():
    scraped_data = []

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.burgerking.in/product-listing")
    time.sleep(4)

    driver.find_element(By.CSS_SELECTOR, ".location-input__value").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//p[contains(text(),'DY Patil Nerul Navi Mumbai')]").click()
    time.sleep(6)
    driver.find_element(By.XPATH, "//div[contains(text(),'See All')]").click()
    time.sleep(7)

    visited = set()

    while True:
        categories = driver.find_elements(By.CSS_SELECTOR, ".menu-tabs__name.menu-tabs__name-ellipsis")
        category_names = [c.text.strip() for c in categories if c.text.strip()]

        clicked_any = False
        for idx, category_name in enumerate(category_names):
            if category_name in visited:
                continue

            try:
                categories = driver.find_elements(By.CSS_SELECTOR, ".menu-tabs__name.menu-tabs__name-ellipsis")
                categories[idx].click()
                visited.add(category_name)
                clicked_any = True
                time.sleep(4)

                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                soup = BeautifulSoup(driver.page_source, "html.parser")
                names = [n.get_text(strip=True) for n in soup.select(".card-gen__name-text")]
                prices = [p.get_text(strip=True) for p in soup.select(".card-gen__currency")]

                for j in range(len(names)):
                    scraped_data.append({
                        "Product": names[j] if j < len(names) else None,
                        "Price": prices[j] if j < len(prices) else None,
                        "Type": category_name,
                        "Location": "DY Patil Nerul Navi Mumbai",
                        "Review_Text": None,
                        "Hashtags": None,
                        "URL": None,
                        "Date": None,
                        "Username": None,
                        "Source": "Burger King Website",
                        "Platform_Type": "Brand Website",
                        "Engagement": None
                    })

                print(f"Scraped {len(names)} items from {category_name}")

            except Exception as e:
                print(f"Error scraping {category_name}: {e}")

        if not clicked_any:
            break

    driver.quit()
    return scraped_data
