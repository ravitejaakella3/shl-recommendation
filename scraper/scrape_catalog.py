from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def scrape_catalog(headless=True):
    url = "https://www.shl.com/solutions/products/product-catalog/"
    driver = None
    products = []

    try:
        print("Setting up Chrome driver...")
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--start-maximized") 
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        driver.get(url)
        
        # Wait for table to load
        print("Waiting for product table...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        # Get all product rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print(f"Found {len(rows)} products")

        for row in rows:
            try:
                # Skip header row
                if row.get_attribute("role") == "columnheader":
                    continue
                    
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 4:
                    continue

                # Get product info
                name_link = cols[0].find_element(By.TAG_NAME, "a")
                name = name_link.text.strip()
                url = name_link.get_attribute("href")
                
                remote = bool(cols[1].find_elements(By.CLASS_NAME, "catalogue__circle"))
                adaptive = bool(cols[2].find_elements(By.CLASS_NAME, "catalogue__circle"))
                
                # Get test types
                test_types = []
                type_spans = cols[3].find_elements(By.CLASS_NAME, "product-catalogue__key")
                for span in type_spans:
                    test_type = span.text.strip()
                    test_types.append(test_type)

                product = {
                    "name": name,
                    "url": url,
                    "remote_testing": remote,
                    "adaptive": adaptive,
                    "test_types": test_types
                }
                products.append(product)
                
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue

        print(f"Successfully processed {len(products)} products")
        
        # Save to JSON file
        with open("data/catalog.json", "w") as f:
            json.dump(products, f, indent=2)
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if driver:
            driver.quit()
            
    return products

if __name__ == "__main__":
    scrape_catalog()



