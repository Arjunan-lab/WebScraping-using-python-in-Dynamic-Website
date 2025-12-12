from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import json

options = Options()
# options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

url = "https://www.amazon.in/s?k=phone"
driver.get(url)

data = []

def extract_products():
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")

    for card in product_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2 span").text
        except:
            title = None

        try:
            price = card.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        except:
            price = None

        try:
            rating = card.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text
        except:
            rating = None

        try:
            link = card.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
        except:
            link = None

        data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "link": link
        })

page = 1
max_pages = 3  # scrape first 3 pages (change as needed)

while page <= max_pages:
    print(f"Scraping Page {page}...")
    extract_products()

    # Pagination
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-next")))
        next_button.click()
        page += 1
        time.sleep(3)
    except:
        print("No more pages.")
        break

driver.quit()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("products.csv", index=False)

# Save to JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("\nScraping Completed!")
print("CSV saved as products.csv")
print("JSON saved as products.json")