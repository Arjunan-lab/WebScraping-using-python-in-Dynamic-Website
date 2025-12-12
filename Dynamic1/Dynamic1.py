from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

url = "https://www.flipkart.com/mobile-phones-store?param=4111&fm=neo%2Fmerchandising&iid=M_900d06b8-b755-41dd-a333-f92860f4be59_1_X1NCR146KC29_MC.AH1NTIJZ241Z&cid=AH1NTIJZ241Z"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

# Scroll down to load more products
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(5)

selector = "div.IKaoWD.pEufOT"
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

cards = driver.find_elements(By.CSS_SELECTOR, selector)

if cards:
    print(f"Found {len(cards)} product cards")
    
    for card in cards:
        try:
            products = card.find_elements(By.CSS_SELECTOR, "div.C5mohy")
            
            for product in products:
                try:
                    name = product.find_element(By.CSS_SELECTOR, "a.pIpigb").text
                    price = product.find_element(By.CSS_SELECTOR, "div.hZ3P6w").text
                    
                    # Only print if both name and price are found
                    if name and price:
                        print(f'Name: {name}\nPrice: {price}\n{"-"*50}')
                        
                except Exception as e:
                    # Skip products with missing elements
                    continue
                    
        except Exception as e:
            print(f"Error processing card: {e}")
            continue
else:
    print("Product cards did not load in time.")

driver.quit()